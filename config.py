import os.path
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'sissens_DB.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = 'UM-BOM-CACHORRO-E-O-SEU-DONO'
