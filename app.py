import json
import os

from db import db
from db import User, Song
from flask import Flask
from flask import request

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
    return success_response( [u.serialize() for u in User.query.all()] )

@app.route("/api/users/", methods=["POST"])
def create_user():
    body = json.loads(request.data)
    name = body.get("name")
    if name is None:
        return failure_response("Invalid fields!")
    new_user = User(name=name)
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)

@app.route("/api/users/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    db.session.delete(user)
    db.session.commit()
    return success_response(user.serialize())

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

@app.route("/api/users/<int:user_id>/requests/")
def get_requests_by_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    return success_response()

@app.route("/api/users/<int:user_id>/requests/", methods=["POST"])
def create_request(user_id):
    body = json.loads(request.data)
    message = body.get("message")
    if message is None:
        return failure_response("Invalid fields!")
    new_request = Request(message=message, completed=False)
    db.session.add(new_request)
    db.session.commit()
    return success_response(new_request.serialize(), 201)

@app.route("/api/users/<int:user_id>/request/<int:request_id>/", methods=["POST"])
def complete_request(user_id, request_id):
    pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)