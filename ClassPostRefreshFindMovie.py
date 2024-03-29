from flask import  request
from flask_restful import Resource
import json
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase

class RefreshFindingMovie(Resource):
    def patch(self):
        data = json.loads(request.data)
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        mycursor.execute("UPDATE Posts SET Posts.isReccommend = 0 WHERE Posts.postId = %s; ",( data['postId']))
        connection.commit()
        connection.close()  
        return 'Recieved'