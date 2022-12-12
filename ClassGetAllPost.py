
import collections
import json
from flask_restful import Resource
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase


class GetAllPost(Resource):
    def get(self):
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        mycursor.execute("SELECT Posts.postId, Posts.userId, Posts.postDetail, Posts.createdDate, Posts.createdTime, users.Username \
            FROM Posts LEFT JOIN Users ON Posts.userId = Users.userId \
            WHERE isDeleted = 0 \
            ORDER BY Posts.createdDate DESC, Posts.createdTime DESC")
        user = mycursor.fetchall()
        connection.commit()
        connection.close()  
        
        #convert to json format
        rowarray_list = []
        for row in user:
            t = (row[0],row[1],row[2],row[3])
            rowarray_list.append(t)
        json.dumps(rowarray_list)

        object_list = []
        for row in user:
            d = collections.OrderedDict()
            d['postId'] = row[0]
            d['userId'] = row[1]
            d['postDetail'] = row[2]
            d['createdDate'] = row[3]
            d['createdTime'] = row[4]
            d['username'] = row[5]
            object_list.append(d)
        l = json.dumps(object_list)
        return json.loads(l)