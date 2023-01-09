import collections
import json
from flask_restful import Resource
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase

class GetMovieByPostId(Resource):
  def get(self,postId): 
    #connect to database
    connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
    mycursor = connection.cursor()
    mycursor.execute("SELECT posts.movieId, movies.movieName FROM posts LEFT JOIN movies ON posts.movieId = movies.movieId WHERE postId = %s",postId)
    movie = mycursor.fetchone()
    connection.commit()
    connection.close()

    d = collections.OrderedDict()
    d['movieId'] = movie[0]
    d['movieName'] = movie[1]

    j = json.dumps(d)
    return json.loads(j)