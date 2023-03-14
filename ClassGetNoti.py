
import collections
import json
from flask_restful import Resource
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase
from flask import request, Response

class GetNotification(Resource):
    def get(self): 
        a = request.args
        args = a.to_dict()
        userId = args.get("userId")
        #connect to database
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        mycursor.execute("\
            SELECT  Notification.notiId, Notification.postId, Notification.receiverId, \
                    Notification.isRead, Notification.NotiType, Notification.createdDate, Notification.createdTime, \
                    Notification.readDate, Notification.readTime, Posts.postDetail, Posts.userId, Users.username \
            FROM Notification \
            LEFT JOIN Posts ON Notification.postId = Posts.postId \
            LEFT JOIN Users ON Posts.userId = Users.userId \
            WHERE receiverId = %s\
            ORDER BY Notification.createdDate DESC, Notification.createdTime DESC;",userId)
        selected_rows = mycursor.fetchall()
        connection.commit()
        connection.close()
        #convert to json format
        rowarray_list = []
        for row in selected_rows:
            t = (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],)
            rowarray_list.append(t)
        json.dumps(rowarray_list)

        object_list = []
        for row in selected_rows:
            d = collections.OrderedDict()
            d['notiId'] = row[0]
            d['postId'] = row[1]
            d['receiverId'] = row[2]
            d['isRead'] = row[3]
            d['notiType'] = row[4]
            d['createdDate'] = row[5]
            d['createdTime'] = row[6]
            d['readDate'] = row[7]
            d['readTime'] = row[8]
            d['postDetail'] = row[9]
            d['userId'] = row[10]
            d['username'] = row[11]
            object_list.append(d)
        l = json.dumps(object_list)
        return json.loads(l)