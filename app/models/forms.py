from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
	nome = StringField("nome", validators=[DataRequired()])
	senha = PasswordField("senha", validators=[DataRequired()])
	lembre_me = BooleanField("lembre-me") 