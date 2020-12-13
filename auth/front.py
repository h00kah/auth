import flask
from flask.globals import request

from .models import *
from .app import db_session
from .forms import *

from .api import getUser, createUser


def frontinit(app):
    @app.route("/signin", methods=["GET"])
    def signin_get():
        form = LoginForm(request.form)
        return flask.render_template('forms/login.html', form=form)

    @app.route("/signin", methods=["POST"])
    def signin_post():
        form = LoginForm(request.form)
        if form.validate():
            try:
                user = getUser(form.email)
                if user.validate(form.password):
                    return flask.redirect("/profile")
            except:
                pass
            flask.flash("Invalid login pair or no such user")
        else:
            flask.flash("Invalid form")
        return flask.redirect("/signin")

    @app.route("/signup", methods=["GET"])
    def signup_get():
        form = RegisterForm(request.form)
        return flask.render_template('forms/register.html', form=form)

    @app.route("/signup", methods=["POST"])
    def signup_post():
        form = RegisterForm(request.form)
        if form.validate():
            createUser(form.email, form.name, form.password)
        return flask.redirect("/signin")

    @app.route("/profile", methods=["GET"])
    def profile():
        return {"success": "not implemented"}