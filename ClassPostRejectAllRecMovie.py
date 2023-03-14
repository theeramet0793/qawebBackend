import collections
import json
from flask_restful import Resource
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase
from flask import request, Response

class RejectReccommendMovie(Resource):
    def post(self): 
        data = json.loads(request.data)
        postId = data['postId']
        
        #connect to database
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        
        mycursor.execute("\
          UPDATE Recmovie\
          SET Recmovie.isReject = 1\
          WHERE Recmovie.postId = %s",(postId))
        connection.commit()
        
        mycursor.execute("\
          UPDATE Posts\
          SET Posts.isReccommend = 0\
          WHERE Posts.postId = %s",(postId))
        connection.commit()
        connection.close()