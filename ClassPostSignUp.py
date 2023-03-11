from flask import  request, Response
from flask_restful import Resource
import json
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase
import collections

class SignUp(Resource):
    def post(self):
        print(request.data)
        data = json.loads(request.data)
        print(data)
        
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword, db=connectionDatabase)
        mycursor = connection.cursor()
        duplicate = mycursor.execute("SELECT username FROM Users WHERE username = %s; ",(data['userName']))
        connection.commit()
        connection.close()
        
        if(duplicate != 0):
            return Response({'Duplicate_username'}, status=409, mimetype='application/json')
        
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword, db=connectionDatabase)
        mycursor = connection.cursor()
        duplicate = mycursor.execute("SELECT email FROM Users WHERE email = %s; ",(data['email']))
        connection.commit()
        connection.close()
        
        if(duplicate != 0):
            return Response("Duplicate_email", status=409, mimetype='application/json')
        
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword, db=connectionDatabase)
        mycursor = connection.cursor()
        affectedRow = mycursor.execute("INSERT INTO Users( userName, email, password ) VALUES ( %s, %s, %s); ",(data['userName'], data['email'], data['password'] ))
        # mycursor.execute("SELECT LAST_INSERT_ID();")
        # last_insert_row = mycursor.fetchone()
        connection.commit()
        connection.close()
        
        # d = collections.OrderedDict()
        # if(last_insert_row):
        #     d['email'] = last_insert_row[2]
        #     d['password'] = last_insert_row[3]
        # l = json.dumps(d)
        
        print(affectedRow)
        if(affectedRow == 1):  
            return 'UserCreated'
        else:
            return 'Failed'