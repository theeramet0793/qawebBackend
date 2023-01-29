
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
        
        searchWord = args.get("searchWord")
        searchType = args.get("searchType")
        searchId = args.get("searchId")
        
        if(searchWord == None or searchWord == ''):
          return Response("searchWord not found", status=404, mimetype='application/json')
        if(searchType == None or searchType == ''):
          return Response("searchType not found", status=404, mimetype='application/json')
        
        sortby = args.get("sortby")
        postType = args.get("type")
        followBy = args.get("followby")
        fetchAmount = args.get("fetchAmount")
        currentAmount = args.get("currentAmount")
        
        sql_order_by = orderBy(sortby)
        sql_where = whereType(postType)
        sql_create_only_follow_cte = create_only_follow_cte(followBy)
        sql_filter_only_follow_post = right_join_for_only_follow_post(followBy)
        sql_create_search_by_tag_cte = create_sql_for_poststags_cte(searchType,searchId)
        sql_filter_search_by_tag_cte = right_join_for_search_by_tag(searchType,searchId)
        sql_where_clause_for_search_by_userId = where_for_search_by_userID(searchType,searchId)
          
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        if(searchType=="USER" or searchType=="TAG"):
          mycursor.execute("WITH cte_upvote(post_Id, upvote_count) AS (           \
                                    SELECT upvote.postId, COUNT(upvote.userId)    \
                                    FROM upvote                                   \
                                    WHERE upvote.isUpvote = 1                     \
                                    GROUP BY upvote.postId                        \
                              ), cte_follow(post_Id, follow_count) AS (           \
                                    SELECT follow.postId, COUNT(follow.userId)    \
                                    FROM follow                                   \
                                    WHERE follow.isFollow = 1                     \
                                    GROUP BY follow.postId                        \
                              )"+sql_create_only_follow_cte+sql_create_search_by_tag_cte+"                                                  \
                            SELECT posts.*, cte_upvote.upvote_count as upvotes,  cte_follow.follow_count as follow\
                            FROM posts \
                            LEFT JOIN cte_upvote ON posts.postId = cte_upvote.post_Id\
                            LEFT JOIN cte_follow ON posts.postId = cte_follow.post_Id\
                            "+sql_filter_only_follow_post+sql_filter_search_by_tag_cte+"  \
                            WHERE posts.isDeleted = 0 "+sql_where_clause_for_search_by_userId+"\
                            "+sql_where+sql_order_by+" LIMIT "+currentAmount+","+fetchAmount,())
        elif(searchType=="POST"):
          keyword = '%'+searchWord+'%'
          sql_filter_by_keyword = ("AND posts.postDetail LIKE ")
          mycursor.execute("WITH cte_upvote(post_Id, upvote_count) AS (           \
                                    SELECT upvote.postId, COUNT(upvote.userId)    \
                                    FROM upvote                                   \
                                    WHERE upvote.isUpvote = 1                     \
                                    GROUP BY upvote.postId                        \
                              ), cte_follow(post_Id, follow_count) AS (           \
                                    SELECT follow.postId, COUNT(follow.userId)    \
                                    FROM follow                                   \
                                    WHERE follow.isFollow = 1                     \
                                    GROUP BY follow.postId                        \
                              )"+sql_create_only_follow_cte+"                                                  \
                            SELECT posts.*, cte_upvote.upvote_count as upvotes,  cte_follow.follow_count as follow\
                            FROM posts \
                            LEFT JOIN cte_upvote ON posts.postId = cte_upvote.post_Id\
                            LEFT JOIN cte_follow ON posts.postId = cte_follow.post_Id\
                            "+sql_filter_only_follow_post+"  \
                            WHERE posts.isDeleted = 0 \
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
    return "ORDER BY lastUpdateDate DESC, lastUpdateTime DESC"
  if(sortby == 'upvote'):
    return "ORDER BY upvotes DESC"
  if(sortby == 'follow'):
    return "ORDER BY follow DESC"

def whereType(type):
  if(type == 'all'):
    return ''
  if(type == 'solved'):
    return "AND movieId IS NOT NULL "
  if(type == 'unsolved'):
    return "AND movieID IS NULL "
  
def create_only_follow_cte(userId):
  if(userId != None and userId != ''):
    return(", cte_onlyfollow(post_Id) AS (\
      SELECT follow.postId \
      FROM follow \
      WHERE follow.isFollow = 1 AND follow.userId ="+userId+" )")
  else:
    return('')
  
def right_join_for_only_follow_post(userId):
    if(userId != None and userId != ''):
      return("RIGHT JOIN cte_onlyfollow ON posts.postId = cte_onlyfollow.post_Id")
    else:
      return('')

def create_sql_for_poststags_cte(searchType,tagId):
  if(searchType=="TAG"):
    return(", cte_tag(post_Id) AS ( \
      SELECT poststags.postId \
      FROM poststags \
      WHERE poststags.tagId = "+tagId+" )" )
  else:
    return('')

def right_join_for_search_by_tag(searchType,tagId):
    if(tagId != None and tagId != '' and searchType=="TAG"):
      return("RIGHT JOIN cte_tag ON posts.postId = cte_tag.post_Id")
    else:
      return('')

def where_for_search_by_userID(searchType,userId):
    if(userId != None and userId != '' and searchType=="USER"):
      return("AND posts.userId = "+userId)
    else:
      return('')