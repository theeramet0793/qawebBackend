from flask import  request, Response
from flask_restful import Resource
import json
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase

class ChangeUsername(Resource):
    def patch(self):
        data = json.loads(request.data)
        
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        mycursor.execute("SELECT Users.username FROM Users WHERE Users.username = %s ",( data['newUsername']))
        duplicateName = mycursor.fetchall()
        connection.commit()
        connection.close()  
        
        if(len(duplicateName)>0):
          return Response("duplicate name", status=409, mimetype='application/json')
        
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        mycursor.execute("UPDATE Users SET Users.username = %s WHERE Users.userId = %s; ",( data['newUsername'], data['userId']))
        connection.commit()
        connection.close()  
        return 'Recieved'