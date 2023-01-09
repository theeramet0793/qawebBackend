import collections
import json
from flask_restful import Resource
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase

class GetSearchMovie(Resource):
    def get(self,searchStr): 
        #connect to database
        str = '%'+searchStr+'%' 
        connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
        mycursor = connection.cursor()
        mycursor.execute("SELECT movies.movieId, movies.movieName\
            FROM movies  \
            WHERE movies.movieName LIKE %s ",str)
        tags = mycursor.fetchall()
        connection.commit()
        connection.close()

        object_list = []
        for row in tags:
            d = collections.OrderedDict()
            d['movieId'] = row[0]
            d['movieName'] = row[1]
            object_list.append(d)
        l = json.dumps(object_list)
        return json.loads(l)  