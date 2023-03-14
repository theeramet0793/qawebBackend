from flask import  request
from flask_restful import Resource
import json
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase
import collections

class AddCommentByUser(Resource):
    def post(self):
        data = json.loads(request.data)
        print(data)
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        mycursor.execute("INSERT INTO Comments(postId, userId, commentDetail, createdDate, createdTime, lastUpdateDate, lastUpdateTime) \
            VALUES (%s, %s, %s, %s, %s, %s, %s); ",(data['postId'], data['userId'], data['commentDetail'], data['date'], data['time'], data['date'], data['time']))
        mycursor.execute("SELECT LAST_INSERT_ID();")
        last_insert_row = mycursor.fetchone()
        connection.commit()
        connection.close()  
        
        d = collections.OrderedDict()
        if( len(last_insert_row) > 0):
            d['commentId'] = last_insert_row[0]


        l = json.dumps(d)
        return json.loads(l)