import collections
import json
from flask_restful import Resource
import pymysql
from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase, movie_poster_path

class GetMovieByPostId(Resource):
  def get(self,postId): 
    #connect to database
    connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword,db=connectionDatabase)
    mycursor = connection.cursor()
    mycursor.execute("SELECT Posts.movieId, Movies.movieName, Movies.moviePoster FROM Posts LEFT JOIN Movies ON Posts.movieId = Movies.movieId WHERE postId = %s",postId)
    movie = mycursor.fetchone()
    connection.commit()
    connection.close()

    d = collections.OrderedDict()
    d['movieId'] = movie[0]
    d['movieName'] = movie[1]
    if(movie[2]):
      d['moviePosterPath'] = moviePosterPathGenerator(movie[2])

    j = json.dumps(d)
    return json.loads(j)

def moviePosterPathGenerator(path):
  return movie_poster_path+path