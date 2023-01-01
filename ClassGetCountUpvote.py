import collections
import json
from flask_restful import Resource
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase

class GetCountUpvote(Resource):
    def get(self,postId): 
        #connect to database
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        mycursor.execute("SELECT upvote.postId, COUNT(upvote.postId) as countUpvote FROM upvote WHERE postId = %s AND isUpvote = 1",(postId))
        post = mycursor.fetchall()
        connection.commit()
        connection.close()

        object_list = []
        for row in post:
            d = collections.OrderedDict()
            d['postId']      = row[0]
            d['upvotes']    = row[1]
            object_list.append(d)
        l = json.dumps(object_list[0])
        return json.loads(l)   