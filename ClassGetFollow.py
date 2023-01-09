import collections
import json
from flask_restful import Resource
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase

class GetFollow(Resource):
    def get(self,postId,userId): 
        #connect to database
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        mycursor.execute("SELECT follow.postId, follow.userId, follow.isFollow FROM follow  WHERE follow.postId = %s AND follow.userId = %s ",(postId, userId))
        follow = mycursor.fetchone()
        connection.commit()
        connection.close()


        d = collections.OrderedDict()
        if(follow != None):
          d['postId']      = follow[0]
          d['userId']      = follow[1]
          d['isFollow']    = convert2boolean(follow[2])
        l = json.dumps(d)
        return json.loads(l) 

def convert2boolean(number):
  if(number == 0):
    return False 
  else:
    return True