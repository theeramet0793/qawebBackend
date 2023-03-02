
import collections
import json
from flask_restful import Resource
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase
from flask import request, Response

class UpdateReccommendMovie(Resource):
    def post(self): 
        a = request.json
        postId = a.get("postId")
        movieList = a.get('movielist')
        #print("json = ",a)
        
        #connect to database
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        for movie in movieList:
          mycursor.execute("\
            INSERT INTO recmovie( postId, movieId, freq)\
            VALUES (%s, %s, %s)",(postId, movie['tmdbId'], movie['freq']))
          connection.commit()
        
        mycursor.execute("\
          UPDATE posts\
          SET posts.isReccommend = 1\
          WHERE posts.postId = %s",(postId))
        connection.commit()
        connection.close()
        