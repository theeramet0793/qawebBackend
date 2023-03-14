import collections
import json
from flask_restful import Resource
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase
from flask import request

class GetUpvote(Resource):
    def get(self): 
        a = request.args
        args = a.to_dict()
        
        userId = args.get("userId")
        postId = args.get("postId")
        
        d = collections.OrderedDict()
        if(userId == None):
          return json.loads(json.dumps(d)) 
        
        #connect to database
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        mycursor.execute("SELECT Upvote.postId, Upvote.userId, Upvote.isUpvote FROM Upvote  WHERE Upvote.postId = %s AND Upvote.userId = %s ",(postId, userId))
        upload = mycursor.fetchone()
        connection.commit()
        connection.close()

        if(upload != None):
          d['postId']      = upload[0]
          d['userId']      = upload[1]
          d['isUpvote']    = convert2boolean(upload[2])
        return json.loads(json.dumps(d)) 

def convert2boolean(number):
  if(number == 0):
    return False 
  else:
    return True