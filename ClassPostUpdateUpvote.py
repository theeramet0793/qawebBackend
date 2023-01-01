from flask import  request
from flask_restful import Resource
import json
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase

class UpdateUpvote(Resource):
    def post(self):
        data = json.loads(request.data)
        print(data)
        if(data['isUpvote'] != None):
          connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword, db=connectionDatabase)
          mycursor = connection.cursor()
          mycursor.execute("SELECT * FROM upvote WHERE postId = %s AND userId = %s",(data['postId'], data['userId']))
          find_result = mycursor.fetchall();
          connection.commit()
          
          if( len(find_result) > 0):
            mycursor.execute("UPDATE upvote SET isUpvote = %s WHERE postId = %s AND userId = %s",(data['isUpvote'], data['postId'], data['userId']))
            connection.commit()
          else:
            mycursor.execute("INSERT INTO upvote( postId, userId, isUpvote) VALUES( %s, %s, %s) ",(data['postId'], data['userId'], data['isUpvote']))
            connection.commit()
            
          connection.commit()
          connection.close() 
          return 'received'
        return 404