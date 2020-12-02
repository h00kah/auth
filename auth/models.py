from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String
# from app import db
import psycopg2

from .__main__ import db, app

engine = create_engine(
    app.config["SQLALCHEMY_DATABASE_URI"],
    echo=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class User(Base):
    __tablename__ = 'Users'

    username = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), primary_key=True)
    password = db.Column(db.String(30))
    pwsalt = db.Column(db.String(128))
    pwhash = db.Column(db.LargeBinary(128))
    hash = db.Column(db.String(4))

    def __init__(self, username=None,
                       email=None,
                       password=None,
                       pwsalt=None,
                       pwhash=None,
                       hash=None):
        self.username = username
        self.email = email
        self.password = password
        self.pwsalt = pwsalt
        self.pwhash = pwhash
        self.hash = hash


# Create tables.
Base.metadata.create_all(bind=engine)
