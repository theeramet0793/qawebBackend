
import collections
import json
from flask_restful import Resource
import pymysql


class GetAllPost(Resource):
    def get(self):
        connection = pymysql.connect(host='sql6.freesqldatabase.com', user='sql6528008', password='ygfdb6iNRv',db='sql6528008')
        mycursor = connection.cursor()
        mycursor.execute("SELECT * FROM TestTable WHERE id > %s",'0')
        user = mycursor.fetchall()
        connection.commit()
        connection.close()  
        
        #convert to json format
        rowarray_list = []
        for row in user:
            t = (row[0],row[1],row[2])
            rowarray_list.append(t)
        json.dumps(rowarray_list)

        object_list = []
        for row in user:
            d = collections.OrderedDict()
            d['Id'] = row[0]
            d['Name'] = row[1]
            d['Age'] = row[2]
            object_list.append(d)
        l = json.dumps(object_list)
        return json.loads(l)