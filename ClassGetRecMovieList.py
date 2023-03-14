import collections
import json
from flask_restful import Resource
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase
from flask import request, Response

class GetReccommendMovieForFrontend(Resource):
    def get(self): 
        a = request.args
        postId = a.get("postId")
        
        #connect to database
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        
        mycursor.execute("\
          SELECT Recmovie.movieId, Movies.movieName\
          FROM  Recmovie\
          LEFT JOIN Movies ON Recmovie.movieId = Movies.movieId  \
          WHERE Recmovie.postId = %s AND Recmovie.isReject = 0\
          ORDER BY Recmovie.freq DESC",(postId))
        movies = mycursor.fetchall()
        connection.commit()
        connection.close()
        
        movie_list = []
        for row in movies:
            d = {
              "movieId":row[0],
              "movieName":row[1]
            }
            movie_list.append(d)

        return_object = {
          "postId":postId,
          "movielist":movie_list
        }
        
        j = json.dumps(return_object)
        return json.loads(j)