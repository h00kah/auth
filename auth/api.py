from bcrypt import gensalt
import flask
import bcrypt
import hashlib
import base64
import json

from .models import *

class WrongUserScheme(Exception):
    pass

class UserExists(Exception):
    pass

class UserNotExists(Exception):
    pass


def getUser(email):
    user = User.get(email)

    if user is None:
        raise UserNotExists()

    user = user._asdict()
    del user["pwhash"]

    return user

def createUser(email, username, pswd):
    salt = bcrypt.gensalt()

    user = User(
        email=email,
        username=username,
        pwsalt=base64.b64encode(salt).decode("ascii"),
        pwhash=bcrypt.hashpw(pswd.encode(), salt),
        hash=hashlib.sha1(email.encode()).hexdigest()[:4])
    
    db_session.add(user)
    db_session.commit()
    

    return getUser(email)


def updateUser(email, username=None, pswd=None):
    user = User.get(email)

    if user is None:
        raise UserNotExists()

    if username is not None:
        user.username = username

    if pswd is not None:
        salt = bcrypt.gensalt()
        user.email =  email,
        user.pwsalt = base64.b64encode(salt).decode("ascii"),
        user.pwhash = bcrypt.hashpw(pswd.encode(), salt),
        user.hash = hashlib.sha1(email.encode()).hexdigest()[:4],

    return getUser(email)


def reraise(fn_or_exc):
    import functools
    def wraps(fn, exc=None):
        @functools.wraps(fn)
        def wrapped(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except Exception as e:
                if exc is not None:
                    raise exc()
                else:
                    raise e
        return wrapped
    if isinstance(fn_or_exc, type):
        return wraps
    return wraps(fn_or_exc)


@app.route("/api/v1/")
def index():
    return {"status": "ok", "map": app.url_map}

@app.route("/api/v1/oauth", methods=["GET"])
def oauth_get():
    raise NotImplementedError()

@app.route("/api/v1/oauth", methods=["POST"])
def oauth_post():
    raise NotImplementedError()

@app.route("/api/v1/manage/user/<email>")
def user_get(email):
    return {"status": "ok", "map": getUser(email)}

@app.route("/api/v1/manage/user", methods=["POST"])
@reraise(WrongUserScheme)
def create_user():
    return {
        "status": "ok",
        "user": createUser(**flask.request.form)
    }

@app.route("/api/v1/manage/user/<email>", methods=["POST"])
@reraise(WrongUserScheme)
def update_user(email):
    return {
        "status": "ok",
        "user": updateUser(**flask.request.form)
    }

@app.route("/api/v1/manage/user/<email>", methods=["DELETE"])
def delete_user(email):
    user = User.get(email)
    udict = user._asdict()
    db_session.delete(user)
    return {"status": "ok", "user": udict}