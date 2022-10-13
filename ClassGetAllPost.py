
import collections
import json
from flask_restful import Resource
import pymysql


class GetAllPost(Resource):
    def get(self):
        return "Test Hello"