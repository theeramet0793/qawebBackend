from flask import  request
from flask_restful import Resource
import json
import pymysql

class SignUp(Resource):
    def post(self):
        print(request.data)
        data = json.loads(request.data)
        print(data)
        connection = pymysql.connect(host='sql6.freesqldatabase.com', user='sql6580445', password='nDWsWTCL6D',db='sql6580445')
        mycursor = connection.cursor()
        affectedRow = mycursor.execute("INSERT INTO Users( UserName, Email, Password ) VALUES ( %s, %s, %s); ",(data['userName'], data['email'], data['password'] ))
        connection.commit()
        connection.close()
        print(affectedRow)
        if(affectedRow == 1):  
            return 'UserCreated'
        else:
            return 'Failed'