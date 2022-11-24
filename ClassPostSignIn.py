from flask import  request, jsonify
from flask_restful import Resource
from datetime import timedelta
from datetime import datetime
import json
import pymysql

secretKey = "questionandanswerwebsiteforfindingmovie";

class SignIn(Resource):
    def post(self):
        data = json.loads(request.data)
        print(data)
        connection = pymysql.connect(host='sql6.freesqldatabase.com', user='sql6580445', password='nDWsWTCL6D',db='sql6580445')
        mycursor = connection.cursor()
        mycursor.execute("SELECT UserId, UserName FROM Users WHERE Email = %s AND Password = %s",(data['email'], data['password']))
        user = mycursor.fetchall()
        #print(userUID[0])
        connection.commit()
        connection.close()  
        print(user)
        if( len(user) != 1 ):
            return 'failed';
        else:
            return 'success'

