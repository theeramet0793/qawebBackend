from flask import  request
from flask_restful import Resource
import json
import pymysql

class SignUp(Resource):
    def post(self):
        data = json.loads(request.data)
        print(data)
        defaultRole = '1'; # RoleId 1 = normal User
        defaultIsActive = '1'; #True
        connection = pymysql.connect(host='localhost', user='root', password='root',db='qadb')
        mycursor = connection.cursor()
        affectedRow = mycursor.execute("INSERT INTO TblUser( UserName, Email, Password, Role, ImageURL, CreatedAt, IsActive) VALUES ( %s, %s, %s, %s, %s, %s, %s); ",(data['userName'], data['email'], data['password'], defaultRole, data['imageURL'], data['createdAt'], defaultIsActive))
        connection.commit()
        connection.close()
        print(affectedRow)
        if(affectedRow == 1):  
            return 'Recieved'
        else:
            return 'Failed'