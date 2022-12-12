from flask import  request, jsonify,  Response
from flask_restful import Resource
from datetime import timedelta
from datetime import datetime
import json
import pymysql
import jwt
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase

secretKey = "questionandanswerwebsiteforfindingmovie";

class SignIn(Resource):
    def post(self):
        data = json.loads(request.data)
        
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        mycursor.execute("SELECT UserId, UserName, Email FROM Users WHERE Email = %s AND Password = %s",(data['email'], data['password']))
        user = mycursor.fetchall()
        connection.commit()
        connection.close()  
        
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        mycursor.execute("SELECT userId, username FROM Users WHERE email = %s ",(data['email']))
        email = mycursor.fetchall()
        connection.commit()
        connection.close() 
        
        if( len(user) != 1 ):
            if( len(email) == 1):
                return Response("Unauthorized_password_incorrect", status=401, mimetype='application/json')
            else:
                return Response("Unauthorized_email_incorrect", status=401, mimetype='application/json')
        else:
            print(user)
            return generate_token(user[0][0],user[0][1],user[0][2])
        
def generate_token(uid,uname,email):
    token = jwt.encode({
    'userId':uid,
    'username':uname,
    'email':email,
    'expiration':str(datetime.utcnow()+timedelta(minutes=60))
    },secretKey)
    return jsonify({'token': token})
        
