from flask import  request
from flask_restful import Resource
import json
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase
import collections

class UpdatePost(Resource):
    def patch(self):
        data = json.loads(request.data)
        print(data)
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword, db=connectionDatabase)
        mycursor = connection.cursor()
        mycursor.execute("UPDATE Posts \
            SET  postDetail = %s,  lastUpdateDate = %s, lastUpdateTime = %s  \
            WHERE postId = %s; ",(data['postDetail'], data['date'],data['time'], data['postId']))
        connection.commit()
        connection.close() 
        return getUpdateData(data['postId'])

def getUpdateData(postId):
    connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword, db=connectionDatabase)
    mycursor = connection.cursor()
    mycursor.execute("SELECT Posts.postId, Posts.userId, Posts.postDetail, Posts.createdDate, Posts.createdTime, users.Username \
    FROM Posts LEFT JOIN Users ON Posts.userId = Users.userId \
    WHERE isDeleted = 0 AND Posts.postId = %s\
    ORDER BY Posts.createdDate DESC, Posts.createdTime DESC",(postId))
    user = mycursor.fetchall()
    connection.commit()
    connection.close()
    
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
