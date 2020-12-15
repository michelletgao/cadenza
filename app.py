import json
import os

from db import db
from db import User, Song, Request, Recommendation
from flask import Flask, request, url_for, session, redirect
from flask import request
from datetime import datetime
import requests
import song

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
    return success_response( [u.basic_serialize() for u in User.query.all()] )

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
    return success_response(new_user.basic_serialize(), 201)

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

@app.route("/api/users/<int:user1_id>/friend/<int:user2_id>/", methods=["POST"])
def friend_user(user1_id, user2_id):
    user1 = User.query.filter_by(id=user1_id).first()
    if user1 is None:
        return failure_response("User not found!")
    user2 = User.query.filter_by(id=user2_id).first()
    if user2 is None:
        return failure_response("User not found!")
    user1.friends.append(user2)
    user2.friends.append(user1)
    db.session.commit()
    return success_response(user1.friend_serialize(), 201)

@app.route("/api/songs/")
def get_songs():
    return success_response( [s.serialize() for s in Song.query.all()] )

@app.route("/api/songs/", methods=["POST"])
def get_song():
    body = json.loads(request.data)
    title = body.get("title")
    artist = body.get("artist")
    if (title is None) and (artist is None):
        return failure_response("Must give at least song/artist!")
    
    # replace spaces in title/artist with +'s
    if title is not None:
        title = title.replace(" ", "+")
    else:
        title = ""
    if artist is not None:
        artist = artist.replace(" ", "+")
    else: 
        artist = ""

    search_results = song.song_search(title + "+" + artist)

    # put song back into form without +'s
    title = title.replace("+", " ").lower()
    artist = artist.replace("+", " ").lower()

    # make sure the song is in the search results
    for s in search_results:
        if ((title != None) and s.get("title").lower() == title) or ((artist != None) and s.get("artist").lower() == artist):
            new_song = Song(title=s.get("title"), artist=s.get("artist"), album=s.get("album"))
            break
    db.session.add(new_song)
    db.session.commit()
    return success_response(new_song.serialize())

@app.route("/api/songs/search/", methods=["POST"])
def search_song():
    body = json.loads(request.data)
    search = body.get("search")
    if search is None:
        return failure_response("Must search something!")
    search = search.replace(" ", "+")
    search_results = song.song_search(search)
    return success_response(search_results)

@app.route("/api/songs/<int:song_id>/")
def get_song_by_id(song_id):
    song = Song.query.filter_by(id=song_id).first()
    if song is None:
        return failure_response("Song not found!")
    return success_response(song.serialize())

@app.route("/api/users/<int:user_id>/songs/<int:song_id>/", methods=["POST"])
def favorite_song(user_id, song_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    song = Song.query.filter_by(id=song_id).first()
    if song is None:
        return failure_response("Song not found in the database!")
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

@app.route("/api/users/requests/<int:request_id>/")
def get_request_by_id(request_id):
    request = Request.query.filter_by(id=request_id).first()
    if request is None:
        return failure_response("Request not found!")
    return success_response(request.serialize())

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

@app.route("/api/users/requests/<int:request_id>/", methods=["POST"])
def end_request(request_id):
    request = Request.query.filter_by(id=request_id).first()
    if request is None:
        return failure_response("Request not found!")

    request.completed = True
    db.session.commit()
    return success_response(request.serialize(), 201)

@app.route("/api/users/requests/<int:request_id>/recommend/<int:song_id>/", methods=["POST"])
def create_recommendation(request_id, song_id):
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
    print("This is the serialized song:" + str(song.serialize()))
    new_recommendation = Recommendation(message=message, song=song, request_id=request_id)
    db.session.add(new_recommendation)
    song.recommendations.append(new_recommendation)
    db.session.commit()
    return success_response(new_recommendation.serialize(), 201)

@app.route("/api/recommendations/<int:rec_id>/")
def get_recommendation_by_id(rec_id):
    rec = Recommendation.query.filter_by(id=rec_id).first()
    if rec is None:
        return failure_response("Recommendation not found!")
    return success_response(rec.serialize())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)