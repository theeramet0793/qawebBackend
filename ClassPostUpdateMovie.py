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
          mycursor.execute("UPDATE posts SET posts.movieId = NULL, posts.isReccommend = 0, posts.lastUpdateDate = %s, posts.lastUpdateTime = %s\
            WHERE posts.postId = %s",(date, time, postId))
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
              connection.commit()
              
        mycursor.execute("SELECT posts.movieId FROM posts WHERE posts.postId = %s",(postId))
        o = mycursor.fetchone()
        connection.commit()
        oldMovieId = None
        print("==>",o)
        if(o):
          oldMovieId = o[0]
        notiType = calNotiType(movieId,oldMovieId)
        
        mycursor.execute("UPDATE posts SET posts.movieId = %s, posts.isReccommend = 1, posts.lastUpdateDate = %s, posts.lastUpdateTime = %s\
          WHERE posts.postId = %s",(movieId, date, time, postId))
        connection.commit()     
                
        mycursor.execute("SELECT follow.userId FROM follow WHERE follow.isFollow = 1 AND follow.postId = %s ",(postId))
        follows = mycursor.fetchall()
        connection.commit()
        if(follows!=None):
          for follow in follows:
            followerId = follow[0]
            mycursor.execute("INSERT \
              INTO notification(postId, receiverId, isRead, notiType, createdDate, createdTime) \
              VALUES(%s,%s,%s,%s,%s,%s) ",(postId,followerId,0,notiType,date,time))
            connection.commit()
          
        connection.close() 
        return 'Updated successful'
      
def calNotiType(newMovieId, oldMovieId):
  if(newMovieId==None or newMovieId==''):
    return "Remove"
  elif((oldMovieId == None or oldMovieId == 0) and newMovieId!=None):
    return "Add"
  elif((oldMovieId!=None or oldMovieId!=0) and newMovieId!=None and oldMovieId!=newMovieId):
    return "Edit"