from flask import  request
from flask_restful import Resource
import json
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase

class AddPostByUser(Resource):
    def post(self):
        data = json.loads(request.data)
        print(data)
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        mycursor.execute("INSERT INTO Posts(userId, postDetail, createdDate, createdTime) \
            VALUES (%s, %s, %s, %s); ",(data['userId'], data['postDetail'], data['date'], data['time']))
        connection.commit()
        connection.close()  
        return 'Recieved'