
import collections
import json
from flask_restful import Resource
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase

class GetSomePost(Resource):
    def get(self,postId): 
        #connect to database
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        
        mycursor.execute("SELECT Posts.postId, Posts.userId, Posts.postDetail, Posts.createdDate,\
            Posts.createdTime, Posts.lastUpdateDate, Posts.lastUpdateTime, Posts.movieId, Posts.isReccommend, Users.Username\
            FROM Posts LEFT JOIN Users ON Posts.userId = Users.userId \
            WHERE Posts.isDeleted = 0 AND Posts.postId = %s",(postId))
        post = mycursor.fetchall()
        connection.commit()
        
        mycursor.execute("SELECT Poststags.tagId, Tags.tagName \
            FROM Poststags LEFT JOIN Tags ON Poststags.tagId = Tags.tagId  \
            WHERE Poststags.postId = %s AND Poststags.isDeleted = 0",(postId))
        taglist = mycursor.fetchall()
        connection.commit()
        connection.close()
        
        tag_list = []
        for row in taglist:
            d = collections.OrderedDict()
            d['tagId'] = row[0]
            d['tagName'] = row[1]
            tag_list.append(d)

        object_list = []
        for row in post:
            d = collections.OrderedDict()
            d['postId'] = row[0]
            d['userId'] = row[1]
            d['postDetail'] = row[2]
            d['createdDate'] = row[3]
            d['createdTime'] = row[4]
            d['lastUpdateDate'] = row[5]
            d['lastUpdateTime'] = row[6]
            d['movieId'] = row[7]
            d['isReccommend'] = row[8]
            d['username'] = row[9]
            d['tagList'] = tag_list
            object_list.append(d)
        l = json.dumps(object_list[0])
        return json.loads(l)   