from flask import  request
from flask_restful import Resource
import json
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase
import collections

class UpdatePost(Resource):
    def patch(self):
        data = json.loads(request.data)
        print(data)
        postId = data['postId']
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword, db=connectionDatabase)
        mycursor = connection.cursor()
        mycursor.execute("UPDATE Posts \
            SET  postDetail = %s,  lastUpdateDate = %s, lastUpdateTime = %s  \
            WHERE postId = %s; ",(data['postDetail'], data['date'],data['time'], postId))
        connection.commit()
        
        mycursor.execute("SELECT poststags.tagId, poststags.isDeleted FROM poststags WHERE poststags.postId = %s",(postId))
        old_tags_list  = map(lambda x: x[0], list(mycursor.fetchall()))
        connection.commit()
        
        new_tag_list = data['tagList']
        newTagSet = set(new_tag_list)
        oldTagSet = set(old_tags_list)
        
        intersec = newTagSet.intersection(oldTagSet)
        new_diff_old = newTagSet.difference(oldTagSet)
        old_diff_new = oldTagSet.difference(newTagSet)
        
        for tagId in intersec:
            mycursor.execute("UPDATE poststags SET poststags.isDeleted = 0 WHERE poststags.postId = %s AND poststags.tagId = %s",(postId, tagId))
            connection.commit()
        for tagId in old_diff_new:
            mycursor.execute("UPDATE poststags SET poststags.isDeleted = 1 WHERE poststags.postId = %s AND poststags.tagId = %s",(postId, tagId))
            connection.commit()
        for tagId in new_diff_old:
            mycursor.execute("INSERT INTO poststags(postId, tagId) VALUES (%s, %s); ",(postId, tagId))
            connection.commit()
        
        connection.close() 
        return 'Updated successful'

