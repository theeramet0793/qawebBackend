
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
from ClassGetProfileImage import GetProfileImage
from ClassGetCommentById import GetCommentById
from ClassGetCommentByPostId import GetCommentByPostId
from ClassGetCountComment import GetCountComment
from ClassGetSearchTag import GetSearchTag

# Class method POST
from ClassPostAddPostByUser import AddPostByUser
from ClassPostComment import AddCommentByUser
from ClassPostDeletePost import DeletePost
from ClassPostDeleteComment import DeleteComment
from ClassPostUpdatePost import UpdatePost
from ClassPostFoundMovieName import FoundMovieName
from ClassPostSignUp import SignUp
from ClassPostSignIn import SignIn
from ClassPostUpdateProfileImg import UpdateProfileImage
from ClassPostUpdateComment import UpdateComment

#===================================================================
#design resource
app = Flask(__name__)
api = Api(app)
CORS(app)
secretKey = "questionandanswerwebsiteforfindingmovie";


# API GET
api.add_resource(GetAllPost,"/posts")
api.add_resource(GetAllSolvedPost,"/GetAllPostSolve")
api.add_resource(GetAllUnsolvedPost,"/GetAllPostUnsolve")
api.add_resource(GetAllComment,"/GetAllComment")
api.add_resource(GetComment,"/GetComment/<int:postId>")
api.add_resource(GetSomePost,"/post/<int:postId>")
api.add_resource(GetMovieName,"/GetMovieName/<int:postID>")
api.add_resource(GetProfileImage,"/profileUrl/<int:userId>")
api.add_resource(GetCommentById,"/commentbyid/<int:commentId>")
api.add_resource(GetCommentByPostId,"/commentbypostid/<int:postId>")
api.add_resource(GetCountComment,"/countcomment/<int:postId>")
api.add_resource(GetSearchTag,"/searchtags/<string:searchStr>")

# API POST
api.add_resource(AddPostByUser,"/post")
api.add_resource(DeletePost,"/deletepost")
api.add_resource(DeleteComment,"/delete/comment")
api.add_resource(UpdatePost,"/updatepost")
api.add_resource(UpdateComment,"/update/comment")
api.add_resource(FoundMovieName,"/FoundMovieName")
api.add_resource(SignUp,"/signup")
api.add_resource(SignIn,"/signin")
api.add_resource(UpdateProfileImage,"/profileUrl")
api.add_resource(AddCommentByUser,"/comment")

if __name__ == "__main__":
    app.run(debug=True)
    #Change debug to flase when deploy