import flask

from ..models import *
from ..app import db_session

from .utils import *


def apiinit(app):
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
        user = User.query.get(email)
        if user:
            udict = user.asdict()
            db_session.delete(user)
            db_session.commit()
            return {"status": "ok", "user": udict}
        return {"status": "ok", "user": None}