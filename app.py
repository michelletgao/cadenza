import json
import os

from db import db
from db import User, Song, Request, Recommendation
from flask import Flask, request, url_for, session, redirect
from datetime import datetime


app = Flask(__name__)
db_filename = "cadenza.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

# generalized response formats
def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code

def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code

@app.route("/")
@app.route("/api/users/")
def get_users():
    return success_response( [u.partial_serialize() for u in User.query.all()] )

@app.route("/api/users/", methods=["POST"])
def create_user():
    body = json.loads(request.data)
    name = body.get("name")
    username = body.get("username")
    if (name is None) | (username is None):
        return failure_response("Invalid fields!")
    new_user = User(name=name, username=username)
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)

@app.route("/api/users/<int:user_id>/")
def get_user_by_id(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    return success_response(user.serialize())

@app.route("/api/users/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    db.session.delete(user)
    db.session.commit()
    return success_response(user.serialize())

@app.route("/api/users/<int:user1_id>/follow/<int:user2_id>/", methods=["POST"])
def follow_user(user1_id, user2_id):
    user1 = User.query.filter_by(id=user1_id).first()
    if user1 is None:
        return failure_response("User not found!")
    user2 = User.query.filter_by(id=user2_id).first()
    if user2 is None:
        return failure_response("User not found!")
    user1.following.append(user2)
    user2.followers.append(user1)
    db.session.commit()
    return success_response(user1.friend_serialize(), 201)

@app.route("/api/songs/")
def get_songs():
    return success_response( [s.serialize() for s in Song.query.all()] )

@app.route("/api/songs/", methods=["POST"])
def create_song():
    body = json.loads(request.data)
    title = body.get("title")
    album = body.get("album")
    artist = body.get("artist")
    if (title is None) | (album is None) | (artist is None):
        return failure_response("Invalid fields!")
    new_song = Song(title=title, album=album, artist=artist)
    db.session.add(new_song)
    db.session.commit()
    return success_response(new_song.serialize(), 201)

@app.route("/api/users/<int:user_id>/songs/<int:song_id>/", methods=["POST"])
def favorite_song(user_id, song_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    song = Song.query.filter_by(id=song_id).first()
    if song is None:
        return failure_response("Song not found!")
    user.fav_songs.append(song)
    db.session.commit()
    return success_response(user.serialize().get("fav_songs"), 201)

@app.route("/api/users/<int:user_id>/requests/")
def get_requests_by_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    requests = user.serialize().get("requests")
    if requests is None:
        return failure_response("No requests found!")
    return success_response(requests)

@app.route("/api/users/<int:user_id>/requests/", methods=["POST"])
def create_request(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    body = json.loads(request.data)
    genre = body.get("genre")
    message = body.get("message")
    if (message is None) | (genre is None):
        return failure_response("Invalid fields!")
    new_request = Request(genre=genre, message=message, timestamp=str(datetime.now()), completed=False, user_id=user_id)
    db.session.add(new_request)
    db.session.commit()
    return success_response(new_request.serialize(), 201)

@app.route("/api/users/<int:user_id>/requests/<int:request_id>/", methods=["POST"])
def end_request(user_id, request_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    request = Request.query.filter_by(id=request_id).first()
    if request is None:
        return failure_response("Request not found!")

    request.completed = True
    db.session.commit()
    return success_response(request.serialize(), 201)

@app.route("/api/users/<int:user_id>/requests/<int:request_id>/recommend/<int:song_id>/", methods=["POST"])
def create_recommendation(user_id, request_id, song_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    req = Request.query.filter_by(id=request_id).first()
    if req is None:
        return failure_response("Request not found!")
    song = Song.query.filter_by(id=song_id).first()
    if song is None:
        return failure_response("Song not found!")

    body = json.loads(request.data)
    message = body.get("message")
    if message is None:
        return failure_response("Invalid fields!")
    new_recommendation = Recommendation(message=message, song=song, request_id=request_id)
    db.session.add(new_recommendation)
    db.session.commit()
    return success_response(new_recommendation.serialize(), 201)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)