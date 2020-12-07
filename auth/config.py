import os
import random
import string

def config():
    basedir = os.path.abspath(os.path.dirname(__file__))

    DEBUG = True

    random.seed(hash('you will never guess my secret'))
    SECRET_KEY = ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))

    if os.path.exists("./production"):
        # We really have to decide what we want to do with password here...
        SQLALCHEMY_DATABASE_URI = 'postgresql:///hookah:529da69ff09daa2f@rc1a-59envrkjvbqtj71y.mdb.yandexcloud.net:6432/hookah'
        SQLALCHEMY_DATABASE_KWA = dict(echo=True)
    else:
        from sqlalchemy.pool import StaticPool
        SQLALCHEMY_DATABASE_URI = 'sqlite://'
        SQLALCHEMY_DATABASE_KWA = dict(echo=True, connect_args={"check_same_thread": False},  poolclass=StaticPool)
    
    return locals()