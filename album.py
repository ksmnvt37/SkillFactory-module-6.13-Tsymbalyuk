import os
import json

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()

class Album(Base):

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)

def connect_db():

    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def find(artist):

    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums

def find_album(album_data):

    year, artist, genre, album = format_it(album_data)
    session = connect_db()
    existing_album = session.query(Album).filter(Album.artist == artist).filter(Album.album == album).first()
    return existing_album

def add_album(album_data):

    year, artist, genre, album = format_it(album_data)
    session = connect_db()
    added_album = Album(year=year, artist=artist, genre=genre, album=album)
    session.add(added_album)
    try:
        session.commit()
    except Exception as e:
        return False
    else:
        return True

def format_it(album_data):
    year = int(album_data["year"])
    artist = album_data["artist"].title()
    genre = album_data["genre"].capitalize()
    album = album_data["album"].title()
    return year, artist, genre, album