
#server side
from flask import Flask
from flask_restful import Api
from flask_cors import CORS

# Class method GET
from ClassGetAllComment import GetAllComment
from ClassGetAllPost import GetAllPost
from ClassGetAllSolvedPost import GetAllSolvedPost
from ClassGetAllUnsolvePost import GetAllUnsolvedPost
from ClassGetMovieName import GetMovieName
from ClassGetComment import GetComment
from ClassGetSomePost import GetSomePost

# Class method POST
from ClassPostAddPostByUser import AddPostByUser
from ClassPostAddCommentByUser import AddCommentByUser
from ClassPostDeletePost import DeletePost
from ClassPostDeleteComment import DeleteComment
from ClassPostUpdatePost import UpdatePost
from ClassPostFoundMovieName import FoundMovieName
from ClassPostSignUp import SignUp
from ClassPostSignIn import SignIn

#===================================================================
#design resource
app = Flask(__name__)
api = Api(app)
CORS(app)
secretKey = "questionandanswerwebsiteforfindingmovie";


# API GET
api.add_resource(GetAllPost,"/GetAllPost")
api.add_resource(GetAllSolvedPost,"/GetAllPostSolve")
api.add_resource(GetAllUnsolvedPost,"/GetAllPostUnsolve")
api.add_resource(GetAllComment,"/GetAllComment")
api.add_resource(GetComment,"/GetComment/<int:postId>")
api.add_resource(GetSomePost,"/GetSomePost/<int:postID>")
api.add_resource(GetMovieName,"/GetMovieName/<int:postID>")

# API POST
api.add_resource(AddPostByUser,"/PostByUser")
api.add_resource(AddCommentByUser,"/CommentByUser")
api.add_resource(DeletePost,"/DeletePost")
api.add_resource(DeleteComment,"/DeleteComment")
api.add_resource(UpdatePost,"/UpdatePost")
api.add_resource(FoundMovieName,"/FoundMovieName")
api.add_resource(SignUp,"/SignUp")
api.add_resource(SignIn,"/signin")

if __name__ == "__main__":
    app.run(debug=False)