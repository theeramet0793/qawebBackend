from flask import  request
from flask_restful import Resource
import json
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase

class UpdateProfileImage(Resource):
    def post(self):
        data = json.loads(request.data)
        print(data)
        if(data['urlPath'] != None):
          connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword, db=connectionDatabase)
          mycursor = connection.cursor()
          mycursor.execute("INSERT INTO profilepic( userId, urlPath, createdDate, createdTime)\
            VALUES( %s, %s, %s, %s) ",(data['userId'], data['urlPath'],data['date'], data['time']))
          connection.commit()
          connection.close() 
          return 'received'
        return 404