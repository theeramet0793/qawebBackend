import collections
import json
from flask_restful import Resource
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase

class GetCommentByPostId(Resource):
    def get(self,postId): 
        #connect to database
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        mycursor.execute("SELECT comments.commentId \
            FROM comments  \
            WHERE isDeleted = 0 AND comments.postId = %s \
            ORDER BY comments.lastUpdateDate DESC, comments.lastUpdateTime DESC, comments.commentId DESC",(postId))
        post = mycursor.fetchall()
        connection.commit()
        connection.close()

        object_list = []
        for row in post:
            d = collections.OrderedDict()
            d['commentId']      = row[0]
            object_list.append(d)
        l = json.dumps(object_list)
        return json.loads(l) 