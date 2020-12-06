from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String, LargeBinary
import psycopg2

from sqlalchemy.pool import StaticPool

from .app import app, db


Base = declarative_base()

engine = create_engine(
    app.config["SQLALCHEMY_DATABASE_URI"],
    echo=True,
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool)

db_session = scoped_session(sessionmaker(autocommit=False,
                                        autoflush=False,
                                        bind=engine))
Base.query = db_session.query_property()

from datetime import datetime
from sqlalchemy.orm import class_mapper

def object_to_dict(obj, found=None):
    if found is None:
        found = set()
    mapper = class_mapper(obj.__class__)
    columns = [column.key for column in mapper.columns]
    get_key_value = lambda c: (c, getattr(obj, c).isoformat()) if isinstance(getattr(obj, c), datetime) else (c, getattr(obj, c))
    out = dict(map(get_key_value, columns))
    for name, relation in mapper.relationships.items():
        if relation not in found:
            found.add(relation)
            related_obj = getattr(obj, name)
            if related_obj is not None:
                if relation.uselist:
                    out[name] = [object_to_dict(child, found) for child in related_obj]
                else:
                    out[name] = object_to_dict(related_obj, found)
    return out

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

    def asdict(self):
        dict = object_to_dict(self)
        del dict["pwhash"]
        del dict["pwsalt"]
        # dict["hash"] = dict["hash"].hex()
        return dict

Base.metadata.create_all(bind=engine)