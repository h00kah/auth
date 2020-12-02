import os

def config():
    # Grabs the folder where the script runs.
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Enable debug mode.
    DEBUG = True

    # Secret key for session management. You can generate random strings here:
    # https://randomkeygen.com/
    SECRET_KEY = 'you will never guess my secret'

    # Connect to the database
    SQLALCHEMY_DATABASE_URI = 'postgresql:///hookah:529da69ff09daa2f@rc1a-59envrkjvbqtj71y.mdb.yandexcloud.net:6432/hookah'
    return locals()