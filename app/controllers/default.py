from flask import render_template, request, redirect, url_for
from app import app, db
from app.models.forms import LoginForm
from app.models.Sissens_DB import Usuario

@app.route("/")
@app.route("/index")
def index():
	return render_template('PainelAdm.html')

@app.route("/login")
def Login():
	form = LoginForm()
	if form.validate_on_submit():
		user = Usuario.query.filter_by(login=form.login.data).first()
		if user and user.senha == form.senha.data:
			login_user(user)
			return redirect(url_for("painelAdm"))
		else:
			flash("Login Inválido. Tente Novamente.")
	else:
		print(form.errors)
	return render_template('login.html', form=form)

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