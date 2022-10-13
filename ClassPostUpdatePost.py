from flask import  request
from flask_restful import Resource
import json
import pymysql

class UpdatePost(Resource):
    def post(self):
        data = json.loads(request.data)
        print(data)
        connection = pymysql.connect(host='localhost', user='root', password='root',db='qadb')
        mycursor = connection.cursor()
        mycursor.execute("UPDATE TblPost SET  PostDetail = %s,  LastUpdate = %s  WHERE PostId = %s; ",(data['postDetail'],data['lastUpdate'],data['postId']))
        connection.commit()
        connection.close()  
        return 'Recieved'