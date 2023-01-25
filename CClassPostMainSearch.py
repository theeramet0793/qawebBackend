
import collections
import json
from flask_restful import Resource
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase
from flask import request


class PostMainSearch(Resource):
    def get(self):

        a = request.args
        args = a.to_dict()
        
        str  = args.get("searchString")
        tagId = args.get("tagId")
        userId  = args.get("userId")
        isKeyword  = args.get("isKeyword")
        searchStr = ''
        
        if(str != None):
          searchStr = '%'+str+'%' 

        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        
        if(tagId != None):
          mycursor.execute("SELECT posts.postId FROM posts  WHERE tags.tagName LIKE %s ",searchStr)
          tags = mycursor.fetchall()
          connection.commit()
        
        mycursor.execute("SELECT users.userId, users.username FROM users  WHERE users.username LIKE %s ",searchStr)
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
          d['userName'] = row[1]
          users_list.append(d)
        
        object_return = {
          "tags":tags_list,
          "users":users_list
        }
        
        l = json.dumps(object_return)
        return json.loads(l)

