import collections
import json
from flask_restful import Resource
import pymysql


class GetMovieName(Resource):
    def get(self,movie_id): 
        #connect to database
        connection = pymysql.connect(host='localhost', user='root', password='root',db='qadb')
        mycursor = connection.cursor()
        mycursor.execute("SELECT * FROM TblMovie WHERE MovieId = %s",movie_id)
        selected_rows = mycursor.fetchall()
        connection.commit()
        connection.close()
         #convert python object to json for post
        rowarray_list = []
        for row in selected_rows:
            t = (row[0],row[1],row[2])
            rowarray_list.append(t)
        json.dumps(rowarray_list)

        object_list = []
        for row in selected_rows:
            d = collections.OrderedDict()
            d['MovieId'] = row[0]
            d['MovieName'] = row[1]
            d['MovieType'] = row[2]
            object_list.append(d)
        j = json.dumps(object_list)
        return json.loads(j)