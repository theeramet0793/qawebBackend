import collections
import json
from flask_restful import Resource
import pymysql
from Const import api_key_for_TMDB
import requests

class GetSearchMovie(Resource):
    def get(self,searchStr): 

        str = '%'+searchStr+'%' 
        data = requests.get('https://api.themoviedb.org/3/search/movie?api_key='+api_key_for_TMDB+'&language=en-EN&query='+str+'&page=1').content 
        return json.loads(data)  
        # object_list = []
        # for row in tags:
        #     d = collections.OrderedDict()
        #     d['movieId'] = row[0]
        #     d['movieName'] = row[1]
        #     object_list.append(d)
        # l = json.dumps(object_list)
        # return json.loads(l)  