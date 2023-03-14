
import collections
import json
from flask_restful import Resource
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase
from flask import request, Response


class GetAllSearchPost(Resource):
    def get(self):
        a = request.args
        args = a.to_dict()
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        
        searchWord = args.get("searchWord")
        searchType = args.get("searchType")
        tag_id = None
        user_id = None
        
        if(searchWord == None or searchWord == ''):
          return Response("searchWord is required", status=404, mimetype='application/json')
        if(searchType == None or searchType == ''):
          return Response("searchType is required", status=404, mimetype='application/json')
        else:
          if(searchType=="TAG"):
            mycursor.execute("SELECT Tags.tagId FROM Tags WHERE Tags.tagName = %s",(searchWord))
            tag= mycursor.fetchone()
            connection.commit()
            if(tag!=None):
              tag_id = str(tag[0])

          elif(searchType =="USER"):
            mycursor.execute("SELECT Users.userId FROM Users WHERE Users.username = %s",(searchWord))
            user = mycursor.fetchone()
            connection.commit()
            if(user!=None):
              user_id = str(user[0])
            
        sortby = args.get("sortby")
        postType = args.get("type")
        followBy = args.get("followby")
        fetchAmount = args.get("fetchAmount")
        currentAmount = args.get("currentAmount")
        
        sql_order_by = orderBy(sortby)
        sql_where = whereType(postType)
        sql_create_only_follow_cte = create_only_follow_cte(followBy)
        sql_filter_only_follow_post = right_join_for_only_follow_post(followBy)
        sql_create_search_by_tag_cte = create_sql_for_poststags_cte(searchType,tag_id)
        sql_filter_search_by_tag_cte = right_join_for_search_by_tag(searchType,tag_id)
        sql_where_clause_for_search_by_userId = where_for_search_by_userID(searchType,user_id)
          
        if(searchType=="USER" or searchType=="TAG"):
          mycursor.execute("WITH cte_upvote(post_Id, upvote_count) AS (           \
                                    SELECT Upvote.postId, COUNT(Upvote.userId)    \
                                    FROM Upvote                                   \
                                    WHERE Upvote.isUpvote = 1                     \
                                    GROUP BY Upvote.postId                        \
                              ), cte_follow(post_Id, follow_count) AS (           \
                                    SELECT Follow.postId, COUNT(Follow.userId)    \
                                    FROM Follow                                   \
                                    WHERE Follow.isFollow = 1                     \
                                    GROUP BY Follow.postId                        \
                              )"+sql_create_only_follow_cte+sql_create_search_by_tag_cte+"                                                  \
                            SELECT Posts.*, cte_upvote.upvote_count as upvotes,  cte_follow.follow_count as follow\
                            FROM Posts \
                            LEFT JOIN cte_upvote ON Posts.postId = cte_upvote.post_Id\
                            LEFT JOIN cte_follow ON Posts.postId = cte_follow.post_Id\
                            "+sql_filter_only_follow_post+sql_filter_search_by_tag_cte+"  \
                            WHERE Posts.isDeleted = 0 "+sql_where_clause_for_search_by_userId+"\
                            "+sql_where+sql_order_by+" LIMIT "+currentAmount+","+fetchAmount,())
        elif(searchType=="POST"):
          keyword = '%'+searchWord+'%'
          sql_filter_by_keyword = ("AND Posts.postDetail LIKE ")
          mycursor.execute("WITH cte_upvote(post_Id, upvote_count) AS (           \
                                    SELECT Upvote.postId, COUNT(Upvote.userId)    \
                                    FROM Upvote                                   \
                                    WHERE Upvote.isUpvote = 1                     \
                                    GROUP BY Upvote.postId                        \
                              ), cte_follow(post_Id, follow_count) AS (           \
                                    SELECT Follow.postId, COUNT(Follow.userId)    \
                                    FROM Follow                                   \
                                    WHERE Follow.isFollow = 1                     \
                                    GROUP BY Follow.postId                        \
                              )"+sql_create_only_follow_cte+"                                                  \
                            SELECT Posts.*, cte_upvote.upvote_count as upvotes,  cte_follow.follow_count as follow\
                            FROM Posts \
                            LEFT JOIN cte_upvote ON Posts.postId = cte_upvote.post_Id\
                            LEFT JOIN cte_follow ON Posts.postId = cte_follow.post_Id\
                            "+sql_filter_only_follow_post+"  \
                            WHERE Posts.isDeleted = 0 \
                            "+sql_where+sql_filter_by_keyword+"%s"+sql_order_by+" LIMIT "+currentAmount+","+fetchAmount,(keyword))
        posts = mycursor.fetchall()
        connection.commit()
        connection.close()  

        object_list = []
        for row in posts:
            d = collections.OrderedDict()
            d['postId'] = row[0]
            object_list.append(d)
        l = json.dumps(object_list)
        return json.loads(l)

def orderBy(sortby):
  if(sortby == 'date'):
    return " ORDER BY lastUpdateDate DESC, lastUpdateTime DESC"
  if(sortby == 'upvote'):
    return " ORDER BY upvotes DESC"
  if(sortby == 'follow'):
    return " ORDER BY follow DESC"

def whereType(type):
  if(type == 'all'):
    return ''
  if(type == 'solved'):
    return " AND movieId IS NOT NULL "
  if(type == 'unsolved'):
    return " AND movieId IS NULL "
  
def create_only_follow_cte(userId):
  if(userId != None and userId != ''):
    return(", cte_onlyfollow(post_Id) AS (\
      SELECT Follow.postId \
      FROM Follow \
      WHERE Follow.isFollow = 1 AND Follow.userId ="+userId+" )")
  else:
    return('')
  
def right_join_for_only_follow_post(userId):
    if(userId != None and userId != ''):
      return(" RIGHT JOIN cte_onlyfollow ON Posts.postId = cte_onlyfollow.post_Id")
    else:
      return('')

def create_sql_for_poststags_cte(searchType,tagId):
  if(searchType=="TAG"):
    if(tagId != None and tagId != ''):
      return(", cte_tag(post_Id) AS ( \
        SELECT Poststags.postId \
        FROM Poststags \
        WHERE Poststags.tagId = "+tagId+" )" )
    else:
      return(", cte_tag(post_Id) AS ( \
        SELECT Poststags.postId \
        FROM Poststags \
        WHERE Poststags.tagId = -1 )" )
  else:
    return('')

def right_join_for_search_by_tag(searchType,tagId):
    if( searchType=="TAG"):
      return(" RIGHT JOIN cte_tag ON Posts.postId = cte_tag.post_Id")
    else:
      return('')

def where_for_search_by_userID(searchType,userId):
    if(searchType=="USER"):
      if(userId != None and userId != ''):
        return(" AND Posts.userId = "+userId)
      else:
        return(" AND Posts.userId = -1")
    else:
      return('')