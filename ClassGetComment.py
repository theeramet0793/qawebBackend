
import collections
import json
from flask_restful import Resource
import pymysql


class GetComment(Resource):
    def get(self,postId): 
        #connect to database
        connection = pymysql.connect(host='localhost', user='root', password='root',db='qadb')
        mycursor = connection.cursor()
        print(postId)
        mycursor.execute("SELECT TblComment.*, TblUser.UserName FROM TblComment Join TblUser On TblComment.CommenterId = TblUser.UserId WHERE TblComment.PostId = %s AND TblComment.IsDeleted = 0;",postId)
        selected_rows = mycursor.fetchall()
        connection.commit()
        connection.close()
        #convert to json format
        rowarray_list = []
        for row in selected_rows:
            t = (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
            rowarray_list.append(t)
        json.dumps(rowarray_list)

        object_list = []
        for row in selected_rows:
            d = collections.OrderedDict()
            d['CommentId'] = row[0]
            d['CommentDetail'] = row[1]
            d['PostId'] = row[2]
            d['CommenterId'] = row[3]
            d['CreatedAt'] = row[4]
            d['LastUpdate'] = row[5]
            d['IsDeleted'] = row[6]
            d['DeletedAt'] = row[7]
            d['CommenterName'] = row[8]
            object_list.append(d)
        l = json.dumps(object_list)
        return json.loads(l)