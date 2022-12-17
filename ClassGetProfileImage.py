
import collections
import json
from flask_restful import Resource
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase
from flask import Response

class GetProfileImage(Resource):
    def get(self,userId): 
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        mycursor.execute("SELECT profilepic.userId, profilepic.urlPath \
          FROM profilepic \
          WHERE profilepic.userId = %s \
          ORDER BY profilepic.createdDate DESC, profilepic.createdTime DESC \
          LIMIT 1;",(userId))
        post = mycursor.fetchall()
        connection.commit()
        connection.close()

        if(len(post) <= 0):
          return Response("No urlPath", status=204, mimetype='application/json')
        
        object_list = []
        for row in post:
            d = collections.OrderedDict()
            d['userId'] = row[0]
            d['urlPath'] = row[1]
            object_list.append(d)
        l = json.dumps(object_list[0])
        return json.loads(l)   