
#server side
from crypt import methods
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_restful import Resource


#===================================================================
#design resource
app = Flask(__name__)
api = Api(app)
CORS(app)
secretKey = "questionandanswerwebsiteforfindingmovie";


class Test(Resource):
    def get(self):
        return "OK"
    
# API GET
api.add_resource(Test,"/Test")
app.route("/", methods=["GET", "POST"])
def home():
    return "Hello"

if __name__ == "__main__":
    app.run()