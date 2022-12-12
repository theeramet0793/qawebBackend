from flask import  request
from flask_restful import Resource
import json
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase

class DeletePost(Resource):
    def patch(self):
        true = '1'
        data = json.loads(request.data)
        print(data)
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        mycursor.execute("UPDATE Posts SET isDeleted = %s, deletedDate = %s, deletedTime = %s, deletedBy = %s WHERE PostId = %s; ",(true, data['deletedDate'], data['deletedTime'], data['deletedBy'], data['postId']))
        connection.commit()
        connection.close()  
        return 'Recieved'