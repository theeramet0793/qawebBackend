import collections
import json
from flask_restful import Resource
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase

class GetSearchTag(Resource):
    def get(self,searchStr): 
        #connect to database
        str = '%'+searchStr+'%' 
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        mycursor.execute("SELECT Tags.tagId, Tags.tagName\
            FROM Tags  \
            WHERE Tags.tagName LIKE %s ",str)
        tags = mycursor.fetchall()
        connection.commit()
        connection.close()

        object_list = []
        for row in tags:
            d = collections.OrderedDict()
            d['tagId'] = row[0]
            d['tagName'] = row[1]
            object_list.append(d)
        l = json.dumps(object_list)
        return json.loads(l)  