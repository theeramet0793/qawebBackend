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
        return 'Updated successful'

