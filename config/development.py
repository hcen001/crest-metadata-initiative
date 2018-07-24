import os

TESTING = True
DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY') or 'not-the-droid-youre-looking-for'

POSTGRES = {
    'user': 'mi_test',
    'pw': 'test',
    'db': 'mi_test',
    'host': '131.94.128.214',
    'port': '5432',
}

SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO=False


TOP_LEVEL_DIR = os.path.abspath(os.curdir)

UPLOADS_DEFAULT_DEST = 'app/static/uploads'
UPLOADS_DEFAULT_URL = 'http://fabian-b:5000/static/uploads/'
