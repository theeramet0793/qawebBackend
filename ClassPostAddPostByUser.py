from flask import  request
from flask_restful import Resource
import json
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase
import collections

class AddPostByUser(Resource):
    def post(self):
        data = json.loads(request.data)
        print(data)
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        mycursor.execute("INSERT INTO Posts(userId, postDetail, createdDate, createdTime, lastUpdateDate, lastUpdateTime) \
            VALUES (%s, %s, %s, %s, %s, %s); ",(data['userId'], data['postDetail'], data['date'], data['time'], data['date'], data['time']))
        mycursor.execute("SELECT LAST_INSERT_ID();")
        last_insert_id = mycursor.fetchone()
        connection.commit()
        
        tagIdList = data['tagList']
        for tagId in tagIdList:
            mycursor.execute("INSERT INTO poststags(postId, tagId) \
            VALUES (%s, %s); ",(last_insert_id, tagId))
            connection.commit()
        connection.close()  
        
        d = collections.OrderedDict()
        if( len(last_insert_id) > 0):
            d['postId'] = last_insert_id[0]
        
        l = json.dumps(d)
        return json.loads(l)
