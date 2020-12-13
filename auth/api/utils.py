import bcrypt
import hashlib
import base64

from auth.models import *
from auth.app import db_session

from .errors import *

def getUser(email):
    user = User.query.get(email)

    if user is None:
        raise UserNotExists()

    user = user.asdict()

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
    user = User.query.get(email)

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

    db_session.commit()

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