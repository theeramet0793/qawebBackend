from flask import  request
from flask_restful import Resource
import json
import pymysql

class AddPostByUser(Resource):
    def post(self):
        data = json.loads(request.data)
        print(data)
        connection = pymysql.connect(host='localhost', user='root', password='root',db='qadb')
        mycursor = connection.cursor()
        mycursor.execute("INSERT INTO TblPost(PostDetail, PosterId, PostType, Movie, CreatedAt, LastUpdate, IsDeleted) VALUES (%s, %s, %s, %s, %s, %s, %s); ",(data['postDetail'], data['posterId'], data['postType'], data['movie'], data['createdAt'], data['lastUpdate'], data['isDeleted']))
        connection.commit()
        connection.close()  
        return 'Recieved'