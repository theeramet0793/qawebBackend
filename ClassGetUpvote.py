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
        mycursor.execute("SELECT upvote.postId, upvote.userId, upvote.isUpvote FROM upvote  WHERE upvote.postId = %s AND upvote.userId = %s ",(postId, userId))
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