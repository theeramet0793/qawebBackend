from flask import  request, jsonify
from flask_restful import Resource
from datetime import timedelta
from datetime import datetime
import json
import pymysql
import jwt

secretKey = "questionandanswerwebsiteforfindingmovie";

class SignIn(Resource):
    def post(self):
        return "ok"