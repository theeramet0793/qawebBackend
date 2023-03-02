
import collections
import json
from flask_restful import Resource
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase
from flask import request, Response

class GetPostByMLSystem(Resource):
    def get(self): 
        #connect to database
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        
        mycursor.execute("\
            SELECT posts.postId, posts.userId, posts.postDetail, posts.createdDate, posts.createdTime, posts.lastUpdateDate, posts.lastUpdateTime, posts.movieId, users.Username\
            FROM posts LEFT JOIN users ON posts.userId = users.userId  \
            WHERE posts.isReccommend = 0\
            ORDER BY posts.lastUpdateDate ASC, posts.lastUpdateTime ASC\
            LIMIT 1",())
        post = mycursor.fetchone()
        connection.commit()

        d = collections.OrderedDict()
        if(post!= None and len(post)>0):
          d['postId'] = post[0]
          d['userId'] = post[1]
          d['postDetail'] = post[2]
          d['createdDate'] = post[3]
          d['createdTime'] = post[4]
          d['lastUpdateDate'] = post[5]
          d['lastUpdateTime'] = post[6]
          d['movieId'] = post[7]
          d['username'] = post[8]
        l = json.dumps(d)
        return json.loads(l)   
    