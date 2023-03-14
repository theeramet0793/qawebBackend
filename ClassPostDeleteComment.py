from flask import  request
from flask_restful import Resource
import json
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase

class DeleteComment(Resource):
    def patch(self):
        true = '1'
        data = json.loads(request.data)
        print(data)
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        mycursor.execute("UPDATE Comments SET isDeleted = %s, deletedDate = %s, deletedTime = %s, deletedBy = %s WHERE commentId = %s; "
                         ,(true, data['date'], data['time'], data['deletedBy'], data['commentId']))
        connection.commit()
        connection.close()  
        return 'Deleted Successful'