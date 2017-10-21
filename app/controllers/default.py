from app import app, db, lm
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from app.models.forms import LoginForm
from app.models.Sissens_DB import Usuario


@lm.user_loader
def load_user(id_User):
	return Usuario.query.filter_by(id_User=id_User).first()

@app.route("/")
@app.route("/index")
def index():
	return render_template('PáginaInicial.html')

@app.route("/login", methods=['GET', 'POST'])
def Login():
	form = LoginForm()
	if form.validate_on_submit():
		user = Usuario.query.filter_by(nome=form.nome.data).first()
		if user and user.senha == form.senha.data and user.perfil == "Adm":
			login_user(user)
			return redirect(url_for("painelAdm"))
		else:
			flash("Login Inválido. Tente Novamente.")
	else:
		print(form.errors)
	return render_template('login.html', form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("index"))

@app.route("/registry")
def Registry():
	return render_template("registerUser.html")

@app.route("/register", methods=['GET', 'POST'])
def Register():
	if request.method == "POST":
		nome = request.form.get("nome")
		perfil = request.form.get("perfil")
		senha = request.form.get("senha")
		email = request.form.get("email")

		if nome and perfil and senha and email:
			u = Usuario(nome,perfil,senha,email)
			db.session.add(u)
			db.session.commit()
		return redirect(url_for("index"))

@app.route("/painelAdm")
def painelAdm():
	return render_template('PainelAdm.html')