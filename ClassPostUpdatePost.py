from flask import  request
from flask_restful import Resource
import json
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase

class UpdatePost(Resource):
    def patch(self):
        data = json.loads(request.data)
        print(data)
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword, db=connectionDatabase)
        mycursor = connection.cursor()
        mycursor.execute("UPDATE Posts SET  postDetail = %s,  lastUpdate = %s  WHERE PostId = %s; ",(data['postDetail'],data['lastUpdate'],data['postId']))
        connection.commit()
        connection.close()  
        return 'Recieved'