from flask import  request
from flask_restful import Resource
import json
import pymysql


class AddCommentByUser(Resource):
    def post(self):
        data = json.loads(request.data)
        print(data)
        connection = pymysql.connect(host='localhost', user='root', password='root',db='qadb')
        mycursor = connection.cursor()
        mycursor.execute("INSERT INTO TblComment( CommentDetail, PostId, CommenterId, CreatedAt, LastUpdate, IsDeleted) VALUES (%s, %s, %s, %s, %s, %s); ",(data['commentDetail'],data['postId'],data['commenterId'],data['createdAt'],data['lastUpdate'],data['isDeleted']))
        connection.commit()
        connection.close()  
        return 'Recieved'