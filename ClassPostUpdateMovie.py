from flask import  request, Response
from flask_restful import Resource
import json
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase
import collections

class UpdateMovie(Resource):
    def patch(self):
        data = json.loads(request.data)
        postId = data['postId']
        movieId = data['movieId']
        movieName = data['movieName']
        userId = data['userId']
        date = data['date']
        time = data['time']
        
        if(postId == None):
          return Response("postId is required", status=404, mimetype='application/json')
        
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword, db=connectionDatabase)
        mycursor = connection.cursor()
        if(len(movieName) <= 0):
          mycursor.execute("UPDATE posts SET posts.movieId = NULL WHERE posts.postId = %s",(postId))
          connection.commit()
        elif(len(movieId) <=0 ):
          return Response("movieId is required", status=404, mimetype='application/json')
        else:
            mycursor.execute("SELECT movies.movieName FROM movies WHERE movies.movieId = %s",(movieId))
            movienamefromDB = mycursor.fetchone()
            connection.commit()
            if(movienamefromDB == None):
              #In case of dont have this movie in DB => Insert new movie 
              mycursor.execute("INSERT INTO movies(movieId, movieName, createdDate, createdTime, createdBy) VALUES(%s, %s, %s, %s, %s)",(movieId, movieName, date, time, userId))
              mycursor.execute("SELECT LAST_INSERT_ID();")
              connection.commit()
              
        mycursor.execute("UPDATE posts SET posts.movieId = %s WHERE posts.postId = %s",(movieId, postId))
        connection.commit()
          
        connection.close() 
        return 'Updated successful'