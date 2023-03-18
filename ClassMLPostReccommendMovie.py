
import collections
import json
from flask_restful import Resource
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase
from flask import request, Response
from datetime import date
from datetime import datetime
import pytz


class UpdateReccommendMovie(Resource):
    def post(self): 
        a = request.json
        postId = a.get("postId")
        userId = a.get('userId')
        movieList = list(a.get('movielist'))
        tz = pytz.timezone('Asia/Bangkok')
        #print("json = ",a)
        
        #connect to database
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword, db=connectionDatabase)
        mycursor = connection.cursor()
        mycursor.execute("\
          SELECT Recmovie.movieId, Recmovie.freq, Recmovie.isReject\
          FROM Recmovie\
          WHERE Recmovie.postId = %s",postId)
        rec_movielist = mycursor.fetchall()
        connection.commit()
        connection.close()
        
        # Find reject movie and duplicate movie 
        reject_id_list = []
        for movie in rec_movielist:
          tmdbId = movie[0]
          freq = movie[1]
          isReject = movie[2] 
          if(isReject == 1):
            reject_id_list.append(tmdbId)
          for m in movieList:
            movieML_id = m['tmdbId']
            movieML_freq = m['freq']
            if(tmdbId == movieML_id and freq == movieML_freq):
              reject_id_list.append(tmdbId)
        
        print(reject_id_list)
        # Filter usable movie 
        usable_movieList = movieList.copy()
        for movie in movieList:
          if(movie['tmdbId'] in reject_id_list):
            #print('remove=',movie)
            usable_movieList.remove(movie)

            
        usable_movieList = usable_movieList[:5]
        #connect to database
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        for movie in usable_movieList:
          mycursor.execute("\
            INSERT INTO Recmovie( postId, movieId, freq)\
            VALUES (%s, %s, %s)",(postId, movie['tmdbId'], movie['freq']))
          connection.commit()
        
        mycursor.execute("\
          UPDATE Posts\
          SET Posts.isReccommend = 1\
          WHERE Posts.postId = %s",(postId))
        connection.commit()
        
        mycursor.execute("INSERT \
          INTO Notification(postId, receiverId, isRead, notiType, createdDate, createdTime) \
          VALUES(%s,%s,%s,%s,%s,%s) ",(postId,userId,0,'RecMov',date.today(),datetime.now(tz).strftime("%H:%M:%S")))
        connection.commit()
        connection.close()
        
        return 'ok'
        