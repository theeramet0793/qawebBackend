
#server side
from flask import Flask
from flask_restful import Api
from flask_cors import CORS

# Class method GET
from ClassGetAllComment import GetAllComment
from ClassGetAllPost import GetAllPost
from ClassGetAllSolvedPost import GetAllSolvedPost
from ClassGetAllUnsolvePost import GetAllUnsolvedPost
from ClassGetMovieByPostId import GetMovieByPostId
from ClassGetComment import GetComment
from ClassGetSomePost import GetSomePost
from ClassGetProfileImage import GetProfileImage
from ClassGetCommentById import GetCommentById
from ClassGetCommentByPostId import GetCommentByPostId
from ClassGetCountComment import GetCountComment
from ClassGetCountUpvote import GetCountUpvote
from ClassGetCountFollow import GetCountFollow
from ClassGetSearchTag import GetSearchTag
from ClassGetSearchMovie import GetSearchMovie
from ClassGetUpvote import GetUpvote
from ClassGetFollow import GetFollow
from ClassGetMainSearch import GetMainSearch
from ClassGetAllSearchPost import GetAllSearchPost
from ClassGetNoti import GetNotification
from ClassMLGetPost import GetPostByMLSystem
from ClassGetRecMovieList import GetReccommendMovieForFrontend

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
from ClassPostUpdateUpvote import UpdateUpvote
from ClassPostUpdateFollow import UpdateFollow
from ClassPostUpdateMovie import UpdateMovie
from ClassPostUpdateNoti import UpdateNotification
from ClassMLPostReccommendMovie import UpdateReccommendMovie
from ClassPostRejectAllRecMovie import RejectReccommendMovie
from ClassPostRefreshFindMovie import RefreshFindingMovie
from ClassPostChangeUsername import ChangeUsername

#===================================================================
#design resource
app = Flask(__name__)
api = Api(app)
CORS(app)
secretKey = "questionandanswerwebsiteforfindingmovie";


# API GET
api.add_resource(GetAllPost,"/posts/") #support {params:{ a:1, b:2}}
api.add_resource(GetAllSolvedPost,"/GetAllPostSolve")
api.add_resource(GetAllUnsolvedPost,"/GetAllPostUnsolve")
api.add_resource(GetAllComment,"/GetAllComment")
api.add_resource(GetComment,"/GetComment/<int:postId>")
api.add_resource(GetSomePost,"/post/<int:postId>")
api.add_resource(GetMovieByPostId,"/getmovie/<int:postId>")
api.add_resource(GetProfileImage,"/profileUrl/<int:userId>")
api.add_resource(GetCommentById,"/commentbyid/<int:commentId>")
api.add_resource(GetCommentByPostId,"/commentbypostid/<int:postId>")
api.add_resource(GetCountComment,"/countcomment/<int:postId>")
api.add_resource(GetCountUpvote,"/countupvote/<int:postId>")
api.add_resource(GetCountFollow,"/countfollow/<int:postId>")
api.add_resource(GetSearchTag,"/searchtags/<string:searchStr>")
api.add_resource(GetSearchMovie,"/searchmovies/<string:searchStr>")
api.add_resource(GetUpvote,"/getUpvote/")
api.add_resource(GetFollow,"/getfollow/<int:postId>/<int:userId>")
api.add_resource(GetMainSearch,"/mainsearch")
api.add_resource(GetAllSearchPost,"/searchposts") #support {params:{ a:1, b:2}}
api.add_resource(GetNotification,"/getnoti")#support {params:{ a:1, b:2}}
api.add_resource(GetPostByMLSystem,"/getonepostformlsystem")
api.add_resource(UpdateReccommendMovie,"/reccommendmovie") #support json
api.add_resource(GetReccommendMovieForFrontend,"/getrecmovielist") #support {params:{ a:1, b:2}}

# API POST/PATCH
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
api.add_resource(UpdateUpvote,"/upvote")
api.add_resource(UpdateFollow,"/follow")
api.add_resource(UpdateMovie,"/updatemovie")
api.add_resource(UpdateNotification,"/marknotiasread")#support {params:{ a:1, b:2}}
api.add_resource(RejectReccommendMovie,"/rejectallreccommendmovie")#support {params:{ a:1, b:2}}
api.add_resource(RefreshFindingMovie,"/refreshFindingMovie")
api.add_resource(ChangeUsername,"/changeusername")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
    #Change debug to flase when deploy