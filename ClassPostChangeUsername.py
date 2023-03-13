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
        mycursor.execute("SELECT users.username FROM users WHERE users.username = %s ",( data['newUsername']))
        duplicateName = mycursor.fetchall()
        connection.commit()
        connection.close()  
        
        if(len(duplicateName)>0):
          return Response("duplicate name", status=409, mimetype='application/json')
        
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        mycursor.execute("UPDATE users SET users.username = %s WHERE users.userId = %s; ",( data['newUsername'], data['userId']))
        connection.commit()
        connection.close()  
        return 'Recieved'