
import collections
import json
from flask_restful import Resource
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase
from flask import request


class GetAllPost(Resource):
    def get(self):
        a = request.args
        args = a.to_dict()
        
        sortby = args.get("sortby")
        postType = args.get("type")
        followBy = args.get("followby")
        fetchAmount = args.get("fetchAmount")
        currentAmount = args.get("currentAmount")
        
        sql_order_by = orderBy(sortby)
        sql_where = whereType(postType)
        sql_create_new_cte = create_new_cte(followBy)
        sql_filter_only_follow_post = right_join_for_only_follow_post(followBy)
          
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
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
                            )"+sql_create_new_cte+"                                                  \
                          SELECT posts.*, cte_upvote.upvote_count as upvotes,  cte_follow.follow_count as follow\
                          FROM posts \
                          LEFT JOIN cte_upvote ON posts.postId = cte_upvote.post_Id\
                          LEFT JOIN cte_follow ON posts.postId = cte_follow.post_Id\
                          "+sql_filter_only_follow_post+"  \
                          WHERE posts.isDeleted = 0 \
                          "+sql_where+sql_order_by+" LIMIT "+currentAmount+","+fetchAmount,())
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
  
def create_new_cte(userId):
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