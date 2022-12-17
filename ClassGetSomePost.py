
import collections
import json
from flask_restful import Resource
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase

class GetSomePost(Resource):
    def get(self,postId): 
        #connect to database
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        mycursor.execute("SELECT Posts.postId, Posts.userId, Posts.postDetail, Posts.createdDate, Posts.createdTime, Posts.lastUpdateDate, Posts.lastUpdateTime, users.Username \
            FROM Posts LEFT JOIN Users ON Posts.userId = Users.userId \
            WHERE isDeleted = 0 AND Posts.postId = %s",(postId))
        post = mycursor.fetchall()
        connection.commit()
        connection.close()

        object_list = []
        for row in post:
            d = collections.OrderedDict()
            d['postId'] = row[0]
            d['userId'] = row[1]
            d['postDetail'] = row[2]
            d['createdDate'] = row[3]
            d['createdTime'] = row[4]
            d['lastUpdateDate'] = row[5]
            d['lastUpdateTime'] = row[6]
            d['username'] = row[7]
            object_list.append(d)
        l = json.dumps(object_list[0])
        return json.loads(l)   