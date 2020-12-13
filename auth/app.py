from gevent import monkey
from werkzeug.utils import HTMLBuilder
monkey.patch_all()

import flask
import functools
import os
import sys

from flask_sqlalchemy import SQLAlchemy
from logging import Formatter, FileHandler

from loguru import logger

from .forms import *
from .config import config

app = flask.Flask(__name__)
app.config.update(config())
db = SQLAlchemy(app)

from .models import *


from .placeholders import placeholdersinit
placeholdersinit(app)

from .api import apiinit
apiinit(app)

from .front import frontinit
frontinit(app)

# Automatically tear down SQLAlchemy.
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()


# Login required decorator.
def login_required(test):
    @functools.wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in flask.session:
            return test(*args, **kwargs)
        else:
            flask.flash('You need to login first.')
            return flask.redirect(flask.url_for('login'))
    return wrap


@app.errorhandler(Exception)
def internal_error(error):
    from werkzeug.exceptions import HTTPException
    #db_session.rollback()

    if isinstance(error, HTTPException):
        return error
    import traceback, sys

    tb = traceback.format_exc(4)
    app.logger.error(tb)
    return {
        "status": "error",
        "error": str(error),
        # TODO: this is not secure! Used for debug and should be removed at release
        "trace": tb,
    }, 500


@app.errorhandler(404)
def not_found_error(error):
    return {"status": "error", "error": "wrong route"}, 404


def run():
    if "--debug" in sys.argv:
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port)
    else:
        from gevent.pywsgi import WSGIServer
        port = os.environ.get('PORT_APP', 5000)
        http_server = WSGIServer(('0.0.0.0', int(port)), app, log=logger)
        http_server.serve_forever()