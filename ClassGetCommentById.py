
import collections
import json
from flask_restful import Resource
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase

class GetCommentById(Resource):
    def get(self,commentId): 
        #connect to database
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        mycursor.execute("SELECT \
            Comments.commentId, Comments.postId, Comments.userId, Comments.commentDetail, Comments.createdDate, Comments.createdTime,\
            Comments.lastUpdateDate, Comments.lastUpdateTime, Users.Username \
            FROM Comments LEFT JOIN Users ON Comments.userId = Users.userId \
            WHERE isDeleted = 0 AND Comments.commentId = %s",(commentId))
        post = mycursor.fetchall()
        connection.commit()
        connection.close()

        object_list = []
        for row in post:
            d = collections.OrderedDict()
            d['commentId']      = row[0]
            d['postId']         = row[1]
            d['userId']         = row[2]
            d['commentDetail']  = row[3]
            d['createdDate']    = row[4]
            d['createdTime']    = row[5]
            d['lastUpdateDate'] = row[6]
            d['lastUpdateTime'] = row[7]
            d['username']       = row[8]
            object_list.append(d)
        l = json.dumps(object_list[0])
        return json.loads(l)   