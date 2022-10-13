from flask import  request
from flask_restful import Resource
import json
import pymysql

class FoundMovieName(Resource):
    def post(self):
        data = json.loads(request.data)
        print(data)
        #ยังต้องเเก้อยู่
        connection = pymysql.connect(host='localhost', user='root', password='root',db='qadb')
        mycursor = connection.cursor()
        mycursor.execute("INSERT INTO TblMovie(PID, movieName) VALUES (%s, %s); ",(data['PID'],data['movieName']))
        connection.commit()
        connection.close()  
        return 'Recieved'