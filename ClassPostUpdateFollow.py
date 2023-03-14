from flask import  request
from flask_restful import Resource
import json
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase

class UpdateFollow(Resource):
    def post(self):
        data = json.loads(request.data)
        print(data)
        if(data['isFollow'] != None):
          connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword, db=connectionDatabase)
          mycursor = connection.cursor()
          mycursor.execute("SELECT * FROM Follow WHERE postId = %s AND userId = %s",(data['postId'], data['userId']))
          find_result = mycursor.fetchall();
          connection.commit()
          
          if( len(find_result) > 0):
            mycursor.execute("UPDATE Follow SET isfollow= %s WHERE postId = %s AND userId = %s",(data['isFollow'], data['postId'], data['userId']))
            connection.commit()
          else:
            mycursor.execute("INSERT INTO Follow( postId, userId, isFollow) VALUES( %s, %s, %s) ",(data['postId'], data['userId'], data['isFollow']))
            connection.commit()
            
          connection.commit()
          connection.close() 
          return 'received'
        return 404