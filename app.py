
#server side
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
api.add_resource(Test,"/")

if __name__ == "__main__":
    app.run(debug=True)