from gevent import monkey
monkey.patch_all()

import flask
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
import os
import sys

from logging import Formatter, FileHandler
from .forms import *
from .config import config
from .placeholders import placeholders
from .api import api

app = flask.Flask(__name__)
app.config.update(config())

placeholders(app)
api(app)

#db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''

@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return flask.render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return flask.render_template('errors/404.html'), 404


if __name__ == '__main__':
    if "--debug" in sys.argv:
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port)
    else:
        from gevent.pywsgi import WSGIServer

        http_server = WSGIServer(('0.0.0.0', int(os.environ['PORT_APP'])), app)
        http_server.serve_forever()