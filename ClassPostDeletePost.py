from flask import  request
from flask_restful import Resource
import json
import pymysql


class DeletePost(Resource):
    def post(self):
        true = '1'
        data = json.loads(request.data)
        print(data)
        connection = pymysql.connect(host='localhost', user='root', password='root',db='qadb')
        mycursor = connection.cursor()
        mycursor.execute("UPDATE TblPost SET IsDeleted = %s, DeletedAt = %s WHERE PostId = %s; ",(true, data['deletedAt'], data['postId']))
        connection.commit()
        connection.close()  
        return 'Recieved'