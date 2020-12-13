from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

user_song_association = db.Table(
    "user_song_association",
    db.Model.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("song_id", db.Integer, db.ForeignKey("song.id"))
)

song_rec_association = db.Table(
    "song_rec_association",
    db.Model.metadata,
    db.Column("song_id", db.Integer, db.ForeignKey("song.id")),
    db.Column("recommendation_id", db.Integer, db.ForeignKey("recommendation.id"))
)

friend_association = db.Table(
    "friend_association",
    db.Model.metadata,
    db.Column("following_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("follower_id", db.Integer, db.ForeignKey("user.id"))
)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    requests = db.relationship("Request", cascade="delete")
    fav_songs = db.relationship("Song", secondary=user_song_association, back_populates="users")
    following = db.relationship("User", secondary=friend_association, 
    primaryjoin=friend_association.c.follower_id==id, secondaryjoin=friend_association.c.following_id==id,
    back_populates="followers")
    followers = db.relationship("User", secondary=friend_association, 
    primaryjoin=friend_association.c.following_id==id, secondaryjoin=friend_association.c.follower_id==id, 
    back_populates="following")

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "")
        self.username = kwargs.get("username", "")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "requests": [r.serialize() for r in self.requests],
            "fav_songs": [s.serialize() for s in self.fav_songs],
        }

    def basic_serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username
        }

    def partial_serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "fav_songs": self.fav_songs
        }

    def friend_serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "following": [f.basic_serialize() for f in self.following],
            "followers": [i.basic_serialize() for i in self.followers]
        }


class Song(db.Model):
    __tablename__ = "song"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    album = db.Column(db.String, nullable=False)
    artist = db.Column(db.String, nullable=False)
    users = db.relationship("User", secondary=user_song_association, back_populates="fav_songs")
    recommendations = db.relationship("Recommendation", secondary=song_rec_association, back_populates="songs")

    def __init__(self, **kwargs):
        self.title = kwargs.get("title", "")
        self.album = kwargs.get("album", "")
        self.artist = kwargs.get("artist", "")

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "album": self.album,
            "artist": self.artist
        }


class Request(db.Model):
    __tablename__ = "request"
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    recommendations = db.relationship("Recommendation", cascade="delete")

    def __init__(self, **kwargs):
        self.genre = kwargs.get("genre", "")
        self.message = kwargs.get("message", "")
        self.timestamp = kwargs.get("timestamp", "")
        self.completed = kwargs.get("completed", "")
        self.user_id = kwargs.get("user_id", "")

    def serialize(self):
        return {
            "id": self.id,
            "genre": self.genre,
            "message": self.message,
            "timestamp": self.timestamp,
            "completed": self.completed,
            "recommendations": [r.serialize() for r in self.recommendations]
        }


class Recommendation(db.Model):
    __tablename__ = "recommendation"
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String, nullable=False)
    request_id = db.Column(db.Integer, db.ForeignKey("request.id"), nullable=False)
    songs = db.relationship("Song", secondary=song_rec_association, back_populates="recommendations")

    def __init__(self, **kwargs):
        self.message = kwargs.get("message", "")
        self.song = kwargs.get("song", "")
        self.request_id = kwargs.get("request_id", "")

    def serialize(self):
        return {
            "id": self.id,
            "message": self.message,
            "song": [s.serialize() for s in self.songs]
        }
