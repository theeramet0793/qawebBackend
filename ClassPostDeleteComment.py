from flask import  request
from flask_restful import Resource
import json
import pymysql


class DeleteComment(Resource):
    def post(self):
        data = json.loads(request.data)
        print(data)
        true = '1'
        connection = pymysql.connect(host='localhost', user='root', password='root',db='qadb')
        mycursor = connection.cursor()
        mycursor.execute("UPDATE TblComment SET IsDeleted = %s, DeletedAt = %s WHERE CommentId = %s; ",(true, data['deletedAt'], data['commentId']))
        connection.commit()
        connection.close()  
        return 'Recieved'