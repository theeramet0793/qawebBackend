
import collections
import json
from flask_restful import Resource
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase
from flask import Response, request

class UpdateNotification(Resource):
    def post(self): 
      #date and time are required!!!
        a = request.args
        args = a.to_dict()
        print(args)
        userId = args.get("userId")
        postId = args.get("postId")
        date = args.get("date")
        time = args.get("time")
        if(postId == None):
          return Response("postId is required", status=404, mimetype='application/json')
        if(userId == None):
          return Response("userId is required", status=404, mimetype='application/json')
        #connect to database
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        mycursor.execute("UPDATE notification\
          SET isRead = 1 , readDate = %s, readTime = %s\
          WHERE postId = %s AND receiverId = %s",(date, time, postId,userId))
        connection.commit()
        connection.close()

        return Response("update successful", status=200, mimetype='application/json')