from flask import Flask 
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class VideoModel(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  views = db.Column(db.Integer, nullable=False)
  likes = db.Column(db.Integer, nullable=False)

  def __repr__(self):
    return f"Video(name={name}, views={views}, likes={likes})"

db.create_all()

videos_put_args = reqparse.RequestParser()
videos_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
videos_put_args.add_argument("views", type=str, help="Views of the video is required", required=True)
videos_put_args.add_argument("likes", type=str, help="Likes of the video is required", required=True)

videos_update_args = reqparse.RequestParser()
videos_update_args.add_argument("name", type=str, help="Name of the video is required")
videos_update_args.add_argument("views", type=str, help="Views of the video is required")
videos_update_args.add_argument("likes", type=str, help="Likes of the video is required")

resourse_fields = {
  "id": fields.Integer, 
  "name": fields.String, 
  "views": fields.Integer, 
  "likes": fields.Integer
}

class Video(Resource): 
  @marshal_with(resourse_fields)
  def get(self, video_id):
    result = VideoModel.query.get({"id": video_id})
    return result

  @marshal_with(resourse_fields)
  def put(self, video_id):
    args =  videos_put_args.parse_args()
    result = VideoModel.query.get({"id": video_id})
    if result:
      abort(409,message='Video id taken...')
    video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
    db.session.add(video)
    db.session.commit()
    return video, 201
  
  @marshal_with(resourse_fields)
  def patch(self, video_id): 
    args =  videos_update_args.parse_args()
    video = VideoModel.query.get({"id": video_id})
    if not video:
      abort(404,message='Video doesnt exist')
    
    for arg in args: 
      if args[arg]:
        setattr(video, arg, args[arg])
  
    db.session.commit()

    return video
    


  def delete(self,video_id):
    abort_if_video_doest_exist(video_id)
    del videos[video_id]
    return '', 204

api.add_resource(Video, '/video/<int:video_id>')

if __name__ == '__main__':
  app.run(debug=True)
