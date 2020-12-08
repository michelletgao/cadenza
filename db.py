from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


user_song_association = db.Table(
    "user_song_association",
    db.Model.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("song_id", db.Integer, db.ForeignKey("song.id"))
)

class Song(db.Model):
    __tablename__ = "song"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    album = db.Column(db.String, nullable=False)
    artist = db.Column(db.String, nullable=False)
    favorite = db.Column(db.Boolean, nullable=False)
    users = db.relationship("Song", secondary=user_song_association, back_populates="songs")

    def __init__(self, **kwargs):
        self.title = kwargs.get("title", "")
        self.album = kwargs.get("album", "")
        self.artist = kwargs.get("artist", "")
        self.favorite = kwargs.get("favorite", "")

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "album": self.album,
            "artist": self.artist,
            "favorite": self.favorite
        }
    
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    requests = db.relationship("Request", cascade="delete")
    fav_songs = db.relationship("Song", secondary=user_song_association, back_populates="users")

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "fav_songs": [s.serialize() for s in self.fav_songs]
        }


class Request(db.Model):
    __tablename__ = "request"
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, **kwargs):
        self.message = kwargs.get("message", "")
        self.completed = kwargs.get("completed", "")

    def serialize(self):
        return {
            "id": self.id,
            "message": self.message,
            "completed": self.completed
        }