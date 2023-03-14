from flask import  request
from flask_restful import Resource
import json
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase
import collections

class UpdateComment(Resource):
    def patch(self):
        data = json.loads(request.data)
        print(data)
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword, db=connectionDatabase)
        mycursor = connection.cursor()
        mycursor.execute("UPDATE Comments \
            SET  commentDetail = %s,  lastUpdateDate = %s, lastUpdateTime = %s  \
            WHERE commentId = %s; ",(data['commentDetail'], data['date'],data['time'], data['commentId']))
        connection.commit()
        connection.close() 
        return 'Updated successful'