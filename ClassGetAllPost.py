
import collections
import json
from flask_restful import Resource
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase


class GetAllPost(Resource):
    def get(self):
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        mycursor.execute("SELECT Posts.postId \
            FROM Posts  \
            WHERE isDeleted = 0 \
            ORDER BY Posts.lastUpdateDate DESC, Posts.lastUpdateTime DESC, Posts.postId DESC")
        user = mycursor.fetchall()
        connection.commit()
        connection.close()  

        object_list = []
        for row in user:
            d = collections.OrderedDict()
            d['postId'] = row[0]
            object_list.append(d)
        l = json.dumps(object_list)
        return json.loads(l)