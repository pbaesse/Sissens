from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from wtforms import StringField, PasswordField, BooleanField
from wtforms.widgets import TextArea
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import date

from wtforms.ext.sqlalchemy.fields import QuerySelectField

app = Flask(__name__)

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

from views import *