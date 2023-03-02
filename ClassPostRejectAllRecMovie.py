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
          UPDATE recmovie\
          SET recmovie.isReject = 1\
          WHERE recmovie.postId = %s",(postId))
        connection.commit()
        
        mycursor.execute("\
          UPDATE posts\
          SET posts.isReccommend = 0\
          WHERE posts.postId = %s",(postId))
        connection.commit()
        connection.close()