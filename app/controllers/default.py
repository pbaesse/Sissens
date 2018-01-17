#teste
from app import app, db, lm
from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from app.models.forms import LoginForm
from app.models.Sissens_DB import Usuario, Tipos_Dpts, Dispositivos


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

		elif user and user.senha == form.senha.data and user.perfil == "Usuario":
			login_user(user)
			return redirect(url_for("painelUsu"))
	else:
		return render_template('login.html', form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("Login"))

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
		return redirect(url_for("painelAdm"))


@app.route("/registerTipoDpt", methods=['GET', 'POST'])
def RegisterTipoDpt():
	if request.method == "POST":
		nome_Tipo_Dpt = request.form.get("nomeTdp")
		descricao = request.form.get("descricao")
		topicos = request.form.get("topicos")

		if nome_Tipo_Dpt and descricao and topicos:
			tipoDisposi = Tipos_Dpts(nome_Tipo_Dpt,descricao,topicos)
			db.session.add(tipoDisposi)
			db.session.commit()
		return redirect(url_for("painelAdm"))

@app.route("/registerDpt", methods=['GET', 'POST'])
def RegisterDpt():

	if request.method == "POST":
		tipo_dpt_Id = request.form.get("tipoDptId")
		nome_Dpt = request.form.get("nomeDpt")
		URL_Foto_Dpt = request.form.get("UrlFoto")

		if tipo_dpt_Id and nome_Dpt and URL_Foto_Dpt:
			disposi = Dispositivos(tipo_dpt_Id,nome_Dpt,URL_Foto_Dpt)
			db.session.add(disposi)
			db.session.commit()
		return redirect(url_for("painelAdm"))

@app.route("/excluir/<int:id>")
def excluir(id):
	usuario = Usuario.query.filter_by(id_User=id).first()
	tipoDpt = Tipos_Dpts.query.all()
	dispositivo = Dispositivos.query.all()
	db.session.delete(usuario)
	db.session.commit()

	usuarios = Usuario.query.all()

	return render_template("PainelAdm.html", usuarios=usuarios, tipoDpt=tipoDpt, dispositivo=dispositivo)

@app.route("/excluirTipoDpt/<int:id>")
def excluirTipoDpt(id):
	DptTipo = Tipos_Dpts.query.filter_by(Tipo_Dpt_id=id).first()
	db.session.delete(DptTipo)
	db.session.commit()

	usuarios = Usuario.query.all()
	tipoDpt = Tipos_Dpts.query.all()
	dispositivo = Dispositivos.query.all()

	return render_template("PainelAdm.html", usuarios=usuarios, tipoDpt=tipoDpt, dispositivo=dispositivo)

@app.route("/excluirDpt/<int:id>")
def excluirDpt(id):
	dpts = Dispositivos.query.filter_by(id_Dpt=id).first()
	db.session.delete(dpts)
	db.session.commit()

	usuarios = Usuario.query.all()
	tipoDpt = Tipos_Dpts.query.all()
	dispositivo = Dispositivos.query.all()

	return render_template("PainelAdm.html", usuarios=usuarios, tipoDpt=tipoDpt, dispositivo=dispositivo)

@app.route("/atualizar/<int:id>", methods=['GET', 'POST'])
def atualizar(id):
	usuarios = Usuario.query.all()
	tipoDpt = Tipos_Dpts.query.all()
	dispositivo = Dispositivos.query.all()
	usuario = Usuario.query.filter_by(id_User=id).first()

	if request.method == "POST":
		nome = request.form.get("nome")
		perfil = request.form.get("perfil")
		senha = request.form.get("senha")
		email = request.form.get("email")

		if nome and perfil and senha and email:
			usuario.nome = nome
			usuario.perfil = perfil
			usuario.senha = senha
			usuario.email = email

			db.session.commit()
		
		return redirect(url_for("painelAdm"))
	
	return render_template("atualizar.html", usuario=usuario, usuarios=usuarios, tipoDpt=tipoDpt, dispositivo=dispositivo)


@app.route("/atualizarTipoDpt/<int:id>", methods=['GET', 'POST'])
def atualizarTipoDpt(id):
	tipoDptss = Tipos_Dpts.query.filter_by(Tipo_Dpt_id=id).first()
	tipoDpt = Tipos_Dpts.query.all()
	usuarios = Usuario.query.all()
	dispositivo = Dispositivos.query.all()

	if request.method == "POST":
		nome_Tipo_Dpt = request.form.get("nomeTdp")
		descricao = request.form.get("descricao")
		topicos = request.form.get("topicos")

		if nome_Tipo_Dpt and descricao and topicos :
			tipoDptss.nome_Tipo_Dpt = nome_Tipo_Dpt
			tipoDptss.descricao = descricao
			tipoDptss.topicos = topicos

			db.session.commit()
		
		return redirect(url_for("painelAdm"))
	
	return render_template("atualizarTipoDpt.html", tipoDptss=tipoDptss, tipoDpt=tipoDpt, usuarios=usuarios, dispositivo=dispositivo)

@app.route("/atualizarDpt/<int:id>", methods=['GET', 'POST'])
def atualizarDpt(id):
	usuarios = Usuario.query.all()
	tipoDpt = Tipos_Dpts.query.all()
	dispositivo = Dispositivos.query.all()
	dpts = Dispositivos.query.filter_by(id_Dpt=id).first()

	if request.method == "POST":
		nome_Dpt = request.form.get("nomeDpt")
		URL_Foto_Dpt = request.form.get("UrlFoto")

		if nome_Dpt and URL_Foto_Dpt:
			dpts.nome_Dpt = nome_Dpt
			dpts.URL_Foto_Dpt = URL_Foto_Dpt

			db.session.commit()
		
		return redirect(url_for("painelAdm"))
	
	return render_template("atualizarDpt.html", dpts=dpts, usuarios=usuarios, tipoDpt=tipoDpt, dispositivo=dispositivo)

@app.route("/painelAdm")
@login_required
def painelAdm():
	usuarios = Usuario.query.all()
	tipoDpt = Tipos_Dpts.query.all()
	dispositivo = Dispositivos.query.all()
	return render_template('PainelAdm.html', usuarios=usuarios, tipoDpt=tipoDpt, dispositivo=dispositivo)

@app.route("/painelUsu")
@login_required
def painelUsu():
		return render_template("PainelUsu.html")


@app.route("/todosDisposi")
def tdsDisposi():
	dispositivo = Dispositivos.query.all()
	usuarios = Usuario.query.all()
	tipoDpt = Tipos_Dpts.query.all()
	return render_template("tdsDisposi.html", dispositivo=dispositivo, usuarios=usuarios, tipoDpt=tipoDpt)

@app.route("/detalhes/<int:id>", methods=['GET', 'POST'])
def detalhes(id):
	dpts = Dispositivos.query.filter_by(id_Dpt=id).first()
	return render_template("detalhesDpt.html", dpts=dpts)





