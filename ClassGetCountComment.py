import collections
import json
from flask_restful import Resource
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase

class GetCountComment(Resource):
    def get(self,postId): 
        #connect to database
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        mycursor.execute("WITH cte_comment(post_id,comment_id) AS (SELECT postId, commentId FROM Comments WHERE postId = %s AND isDeleted = 0)\
          SELECT cte_comment.post_id, COUNT(cte_comment.comment_id) As Comments FROM cte_comment",(postId))
        post = mycursor.fetchall()
        connection.commit()
        connection.close()

        object_list = []
        for row in post:
            d = collections.OrderedDict()
            d['postId']      = row[0]
            d['comments']    = row[1]
            object_list.append(d)
        l = json.dumps(object_list[0])
        return json.loads(l)   