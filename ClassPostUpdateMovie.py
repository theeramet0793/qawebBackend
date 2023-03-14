from flask import  request, Response
from flask_restful import Resource
import json
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase, api_url_for_add_movie_to_ML
import collections
import requests
from FuncUpdatePostDataToML import updateDataToML 

class UpdateMovie(Resource):
    def patch(self):
        data = json.loads(request.data)
        postId = data['postId']
        movieId = data['movieId']
        movieName = data['movieName']
        moviePoster = data['posterPath']
        userId = data['userId']
        date = data['date']
        time = data['time']
        
        if(postId == None):
          return Response("postId is required", status=404, mimetype='application/json')
        
        if(moviePoster == None):
          moviePoster = '';
        
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword, db=connectionDatabase)
        mycursor = connection.cursor()
        if(len(movieName) <= 0):
          # In case of delete movie from post
          mycursor.execute("UPDATE Posts SET Posts.movieId = NULL, Posts.isReccommend = 0, Posts.lastUpdateDate = %s, Posts.lastUpdateTime = %s\
            WHERE Posts.postId = %s",(date, time, postId))
          connection.commit()
        elif(len(movieId) <=0 ):
          return Response("movieId is required", status=404, mimetype='application/json')
        else:
            mycursor.execute("SELECT Movies.movieName FROM Movies WHERE Movies.movieId = %s",(movieId))
            movienamefromDB = mycursor.fetchone()
            connection.commit()
            if(movienamefromDB == None):
              # In case of dont have this movie in DB => Insert new movie 
              mycursor.execute("INSERT INTO Movies(movieId, movieName, moviePoster, createdDate, createdTime, createdBy) VALUES(%s, %s, %s, %s, %s, %s)",(movieId, movieName, moviePoster, date, time, userId))
              connection.commit()
              # add new movie to ML 
              body = {
                "tmdbId":movieId,
                "movieName":movieName,
              }
              requests.post(api_url_for_add_movie_to_ML, json=body)
              
        # For noti
        mycursor.execute("SELECT Posts.movieId FROM Posts WHERE Posts.postId = %s",(postId))
        o = mycursor.fetchone()
        connection.commit()
        oldMovieId = None
        print("==>",o)
        if(o):
          oldMovieId = o[0]
        notiType = calNotiType(movieId,oldMovieId)
        
        # Update post when user select movie name
        if(len(movieName) > 0):
          mycursor.execute("UPDATE Posts SET Posts.movieId = %s, Posts.isReccommend = 1, Posts.lastUpdateDate = %s, Posts.lastUpdateTime = %s\
            WHERE Posts.postId = %s",(movieId, date, time, postId))
          connection.commit()   
        
        # Update post to ML
        updateDataToML(postId)
        
        # Create notification      
        mycursor.execute("SELECT Follow.userId FROM Follow WHERE Follow.isFollow = 1 AND Follow.postId = %s ",(postId))
        follows = mycursor.fetchall()
        connection.commit()
        if(follows!=None):
          for follow in follows:
            followerId = follow[0]
            mycursor.execute("INSERT \
              INTO Notification(postId, receiverId, isRead, notiType, createdDate, createdTime) \
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