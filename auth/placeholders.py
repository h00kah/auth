import flask

from .forms import *

def placeholders(app: flask.Flask):
    @app.route('/')
    def home():
        return flask.render_template('pages/placeholder.home.html')


    @app.route('/about')
    def about():
        return flask.render_template('pages/placeholder.about.html')


    @app.route('/login')
    def login():
        form = LoginForm(flask.request.form)
        return flask.render_template('forms/login.html', form=form)


    @app.route('/register')
    def register():
        form = RegisterForm(flask.request.form)
        return flask.render_template('forms/register.html', form=form)


    @app.route('/forgot')
    def forgot():
        form = ForgotForm(flask.request.form)
        return flask.render_template('forms/forgot.html', form=form)