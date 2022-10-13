
import collections
import json
from flask_restful import Resource
import pymysql


class GetAllUnsolvedPost(Resource):
    def get(self):
        connection = pymysql.connect(host='localhost', user='root', password='root',db='qadb')
        mycursor = connection.cursor()
        mycursor.execute("SELECT * FROM TblPost WHERE PostType = 2 ")
        selected_rows = mycursor.fetchall()
        connection.commit()
        connection.close()
        #convert python object to json for post
        rowarray_list = []
        for row in selected_rows:
            t = (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
            rowarray_list.append(t)
        json.dumps(rowarray_list)

        object_list = []
        for row in selected_rows:
            d = collections.OrderedDict()
            d['PostId'] = row[0]
            d['PostDetail'] = row[1]
            d['PosterId'] = row[2]
            d['PostType'] = row[3]
            d['Movie'] = row[4]
            d['CreatedAt'] = row[5]
            d['LastUpdate'] = row[6]
            d['IsDeleted'] = row[7]
            object_list.append(d)
        j = json.dumps(object_list)
        return json.loads(j)