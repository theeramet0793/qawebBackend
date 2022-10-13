from flask import  request, jsonify
from flask_restful import Resource
from datetime import timedelta
from datetime import datetime
import json
import pymysql
import jwt

secretKey = "questionandanswerwebsiteforfindingmovie";

class SignIn(Resource):
    def post(self):
        data = json.loads(request.data)
        print(data)
        connection = pymysql.connect(host='localhost', user='root', password='root',db='qadb')
        mycursor = connection.cursor()
        mycursor.execute("SELECT UserId, UserName, Role, RoleName FROM TblUser JOIN TblUserrole ON TblUser.Role = TblUserrole.RoleId WHERE Email = %s AND Password = %s",(data['email'], data['password']))
        user = mycursor.fetchall()
        #print(userUID[0])
        connection.commit()
        connection.close()  
        print(user)
        if( len(user) != 1 ):
            return 'failed';
        else:
            return generate_token(user[0][0],user[0][1],user[0][2])

def generate_token(uid,uname,urole):
    token = jwt.encode({
        'UID':uid,
        'UName':uname,
        'URole':urole,
        'expiration':str(datetime.utcnow()+timedelta(minutes=60))
        },secretKey)
    return jsonify({'UID': uid,'UName': uname,'URole':urole,'token': token})