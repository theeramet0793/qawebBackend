from Const import connectionHost, connectionUser, connectionPassword, connectionDatabase, api_url_for_update_post_to_ML
import pymysql
import requests

def updateDataToML(postId):
    if(postId):
      connection = pymysql.connect(host=connectionHost, user=connectionUser, password=connectionPassword, db=connectionDatabase)
      mycursor = connection.cursor()
      mycursor.execute("\
        SELECT Posts.postId, Posts.movieId, Posts.postDetail\
        FROM Posts\
        WHERE Posts.postId = %s",(postId))
      post = mycursor.fetchone()
      connection.commit()
      
      tmdbId = post[1]
      if(tmdbId == None):
        tmdbId = 0;
      body = {
        "postId":post[0],
        "tmdbId":tmdbId,
        "postDetail":post[2],
      }
      requests.post(api_url_for_update_post_to_ML, json=body)