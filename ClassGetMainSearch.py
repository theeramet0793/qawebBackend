
import collections
import json
from flask_restful import Resource
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase
from flask import request


class GetMainSearch(Resource):
    def get(self):

        a = request.args
        args = a.to_dict()
        
        str  = args.get("searchString")
        searchStr = ''
        if(str != None):
          searchStr = '%'+str+'%' 

        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        
        mycursor.execute("SELECT Tags.tagId, Tags.tagName FROM Tags  WHERE Tags.tagName LIKE %s LIMIT 3",searchStr)
        tags = mycursor.fetchall()
        connection.commit()
        
        mycursor.execute("SELECT Users.userId, Users.username FROM Users  WHERE Users.username LIKE %s LIMIT 2",searchStr)
        users = mycursor.fetchall()
        connection.commit()
        
        connection.close()  

        tags_list = []
        for row in tags:
          d = collections.OrderedDict()
          d['tagId'] = row[0]
          d['tagName'] = row[1]
          tags_list.append(d)
            
        users_list = []
        for row in users:
          d = collections.OrderedDict()
          d['userId'] = row[0]
          d['username'] = row[1]
          users_list.append(d)
        
        object_return = {
          "tags":tags_list,
          "users":users_list
        }
        
        l = json.dumps(object_return)
        return json.loads(l)

