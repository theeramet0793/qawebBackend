import collections
import json
from flask_restful import Resource
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase

class GetUpvote(Resource):
    def get(self,postId,userId): 
        #connect to database
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        mycursor.execute("SELECT upvote.postId, upvote.userId, upvote.isUpvote FROM upvote  WHERE upvote.postId = %s AND upvote.userId = %s ",(postId, userId))
        upload = mycursor.fetchall()
        connection.commit()
        connection.close()

        object_list = []
        for row in upload:
            d = collections.OrderedDict()
            d['postId']      = row[0]
            d['userId']      = row[1]
            d['isUpvote']    = convert2boolean(row[2])
            object_list.append(d)
        l = json.dumps(object_list[0])
        return json.loads(l) 

def convert2boolean(number):
  if(number == 0):
    return False 
  else:
    return True