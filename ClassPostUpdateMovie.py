from flask import  request, Response
from flask_restful import Resource
import json
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase
import collections

class UpdateMovie(Resource):
    def patch(self):
        data = json.loads(request.data)
        print(data)
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
        else:
          if(len(movieId) <=0 ):
              #Insert new movie name
              mycursor.execute("INSERT INTO movies(movieName, createdDate, createdTime, createdBy) VALUES(%s, %s, %s, %s)",(movieName, date, time, userId))
              mycursor.execute("SELECT LAST_INSERT_ID();")
              last_insert_id = mycursor.fetchone()
              movieId = last_insert_id[0]
              connection.commit()
          else:
            mycursor.execute("SELECT movies.movieName FROM movies WHERE movies.movieId = %s",(movieId))
            movienamefromDB = mycursor.fetchone()
            connection.commit()
            if(movieName != movienamefromDB[0]):
              #Insert new movie name
              mycursor.execute("INSERT INTO movies(movieName, createdDate, createdTime, createdBy) VALUES(%s, %s, %s, %s)",(movieName, date, time, userId))
              mycursor.execute("SELECT LAST_INSERT_ID();")
              last_insert_id = mycursor.fetchone()
              movieId = last_insert_id[0]
              connection.commit()
              
          mycursor.execute("UPDATE posts SET posts.movieId = %s WHERE posts.postId = %s",(movieId, postId))
          connection.commit()
          
        connection.close() 
        return 'Updated successful'