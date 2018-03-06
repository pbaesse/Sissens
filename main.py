from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.widgets import TextArea
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
#from flask_admin import Admin
#from flask_admin import BaseView, expose
#from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import date

from wtforms.ext.sqlalchemy.fields import QuerySelectField

##################conexao
import eventlet
import json
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap

eventlet.monkey_patch()
##################conexao

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///admin.db'
app.config['SECRET_KEY'] = 'thisisupposedtobesecret!'

##################conexao
app.config['SECRET'] = 'my secret key'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False

mqttt = Mqtt(app)
socketio = SocketIO(app)
###################conexao

Bootstrap(app)
db = SQLAlchemy(app) # obj de acesso ao
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
admin= Admin(app, template_mode="Bootstrap3")

class Usuario(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String(50))
	perfil = db.Column(db.Boolean) #true=adm
	email = db.Column(db.String(50), unique= True)
	senha = db.Column(db.String(50), unique= True)

class Tipodispositivo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	descricao = db.Column(db.String(200))
	tipodeDado =  db.Column(db.String(200))

class Dadosdisp(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	dispositivo_id = db.Column(db.Integer, db.ForeignKey('dispositivo.id'))
	data = db.Column(db.String(80))
	status = db.Column(db.Boolean)
	dados = db.Column(db.Integer)

class Dispositivo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	tipoDispositivo_id = db.Column(db.Integer, db.ForeignKey('tipodispositivo.id'))
	name = db.Column(db.String(50))
	topico = db.Column(db.String(50))
	

class RelacaoDispUsu(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
	dispositivo_id = db.Column(db.Integer, db.ForeignKey('dispositivo.id'))


#########################################################


@login_manager.user_loader
def load_user(user_id):
	return Usuario.query.get(int(user_id))

class LoginForm(FlaskForm):
	email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'),Length(max=50)])
	senha = PasswordField('Senha', validators=[InputRequired(), Length(min=8, max =80)])
	
class RegistrarForm(FlaskForm):
	nome = StringField('Nome', validators=[InputRequired(), Length(min=4, max =15)])
	senha = PasswordField('Senha', validators=[InputRequired(), Length(min=8, max =80)])
	email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'),Length(max=50)])

class RegistrarUsu(FlaskForm):
	nome = StringField('Nome', validators=[InputRequired(), Length(min=4, max =15)])
	senha = PasswordField('Senha', validators=[InputRequired(), Length(min=8, max =80)])
	email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'),Length(max=50)])
	perfil = BooleanField('adm')

class RegistrarDispositivo(FlaskForm):
	name = StringField('Nome', validators=[InputRequired(), Length(max =15)])
	tipoDispositivo_id = StringField('Tipo do dispositivo', validators=[InputRequired(), Length(max =80)])
	topico = StringField('Topico', validators=[InputRequired(),Length(max=50)])

class RegistrarRelacao(FlaskForm):
	dispositivo_id = StringField('ID do dispositivo', validators=[InputRequired(), Length(max =15)])
	usuario_id = StringField('ID do usuario', validators=[InputRequired(), Length(max =80)])
	
	
class RegistraTipodispositivo(FlaskForm):
	name = StringField('Nome', validators=[InputRequired(), Length(max =15)])
	descricao = StringField('Descricao', validators=[InputRequired(), Length(max =80)])
	tipodeDado = StringField('Tipo de dado', validators=[InputRequired(), Length(max =80)])

##################conexao
@socketio.on('publish')
def handle_publish(json_str):
    data = json.loads(json_str)
    mqttt.publish(data['topic'], data['message'])


@socketio.on('subscribe')
def handle_subscribe(json_str):
    data = json.loads(json_str)
    mqttt.subscribe(data['topic'])


@mqttt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    socketio.emit('mqtt_message', data=data)


@mqttt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)
##################conexao

@app.route('/', methods=['GET','POST'])
def index():

	form = LoginForm()
	#if form.validate_on_
	usuario = Usuario.query.filter_by(email=form.email.data).first()
	if usuario:		#compara o hash do banco com a transformacao da senha passa em hash
			#if check_password(usuario.senha, form.senha.data):
		if request.method == "POST":
			if usuario.email == request.form.get("email") and usuario.senha == request.form.get("senha") and usuario.perfil == True:
				login_user(usuario)
				return redirect(url_for('painelAdm'))

			if usuario.email == request.form.get("email") and usuario.senha == request.form.get("senha") and usuario.perfil == False:
				login_user(usuario)
				return redirect(url_for('painelUsu'))
			
	if "root@root.com" == request.form.get("email") and "rootroot" == form.senha.data:
		return redirect(url_for('cadastro'))

	

	return render_template('index.html', form=form)

@app.route('/sobre')
def sobre():
	return render_template('sobre.html')

@app.route('/cadastro', methods=['GET','POST'])
def cadastro():
	form = RegistrarForm()

	if form.validate_on_submit():
		new_user = Usuario(nome=form.nome.data, email=form.email.data, senha=form.senha.data, perfil=True)
		#new_user = User(username=form.username.data, email=form.username.data, password=form.password.data)
		db.session.add(new_user)
		db.session.commit()

		

	return render_template('cadastro.html', form=form)

@app.route("/painelAdm")
@login_required
def painelAdm():
	usuarios = Usuario.query.all()
	tipoDpt = Tipodispositivo.query.all()
	dispositivo = Dispositivo.query.all()
	perfil = "admin"

	return render_template('painelAdm.html', usuarios=usuarios, tipoDpt=tipoDpt, dispositivo=dispositivo, perfil=perfil)

@app.route("/dispositivo/<int:id>", methods=['GET'])
def dispositivo(id):
	dispositivo= Dispositivo.query.get(id)
	x=dispositivo.topico
	return render_template('dispositivo.html', dispositivo=dispositivo)


@app.route("/painelUsu")
@login_required
def painelUsu():
	idlogado = current_user.id
	dispositivo = Dispositivo.query.filter_by(id=2)
	#relacao= relacoes.usuario_id
	#dispositivo = Dispositivo.query.filter_by(id=relacoes.dispositivo_id)
	#perfil = "usuario"

	return render_template('painelUsu.html', dispositivo=dispositivo)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/dispositivoCompleto/<int:id>', methods=['GET','POST'])
def abrirTexto(id):
	#texto = Texto.query.filter_by(id=id).first()
	dispositivo = Dispositivo.query.get(id)
	nome=dispositivo.name
	id= dispositivo.id

	return render_template('dispositivoCompleto.html', nome=nome, id=id )

@app.route("/register", methods=['GET', 'POST'])
def Register():
	form = RegistrarUsu()

	if form.validate_on_submit():

		new_user = Usuario(nome=form.nome.data, email=form.email.data, senha=form.senha.data, perfil=form.perfil.data)
		#new_user = User(username=form.username.data, email=form.username.data, password=form.password.data)
		db.session.add(new_user)
		db.session.commit()
		return "deu certo"
	
	return render_template("tablesUsu.html", form=form)


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
			disposi = Dispositivo(tipo_dpt_Id,nome_Dpt,URL_Foto_Dpt)
			db.session.add(disposi)
			db.session.commit()
		return redirect(url_for("painelAdm"))

@app.route("/excluir/<int:id>")
def excluir(id):
	usuario = Usuario.query.filter_by(id=id).first()
	db.session.delete(usuario)
	db.session.commit()

	usuario = Usuario.query.all()
	form = RegistrarUsu()

	return render_template("tablesUsu.html", usuario=usuario, form=form)

@app.route("/excluirTipoDpt/<int:id>")
def excluirTipoDpt(id):
	DptTipo = Tipodispositivo.query.filter_by(id=id).first()
	db.session.delete(DptTipo)
	db.session.commit()
	tipoDpt = Tipodispositivo.query.all()
	form = RegistrarTipoDpt()

	return render_template("tablesTiposDisp.html", tipoDpt=tipoDpt, form=form)

@app.route("/excluirDpt/<int:id>")
def excluirDpt(id):
	dpts = Dispositivo.query.filter_by(id=id).first()
	db.session.delete(dpts)
	db.session.commit()
	dispositivo = Dispositivo.query.all()

	form = RegistrarDispositivo()	
	return render_template("tablesDisp.html", dispositivo=dispositivo, form=form)

@app.route("/excluirRelacao/<int:id>")
def excluirRelacao(id):
	rls = RelacaoDispUsu.query.filter_by(id=id).first()
	db.session.delete(rls)
	db.session.commit()
	relacao = RelacaoDispUsu.query.all()
	form = RegistrarRelacao()

	return render_template("tablesRelacio.html", relacao=relacao, form=form)

@app.route("/atualizar/<int:id>", methods=['GET', 'POST'])
def atualizar(id):
	usuario = Usuario.query.filter_by(id=id).first()
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
		
		return redirect(url_for("tablesUsu"))
	
	return render_template("atualizar.html", usuario=usuario)

@app.route("/atualizarTipoDpt/<int:id>", methods=['GET', 'POST'])
def atualizarTipoDpt(id):
	tipoDptss = Tipodispositivo.query.filter_by(id=id).first()

	if request.method == "POST":
		name= request.form.get("nome")
		descricao = request.form.get("descricao")
		tipodeDado = request.form.get("tipo")

		if name and descricao and tipodeDado:
			tipoDptss.name = name
			tipoDptss.descricao = descricao
			tipoDptss.tipodeDado = tipodeDado

		db.session.commit()
		
		return redirect(url_for("tablesTiposDisp"))
	
	return render_template("atualizarTiposDpts.html", tipoDptss=tipoDptss)

@app.route("/atualizarDpt/<int:id>", methods=['GET', 'POST'])
def atualizarDpt(id):
	dispositivo = Dispositivo.query.all()
	dpts = Dispositivo.query.filter_by(id=id).first()

	if request.method == "POST":
		name = request.form.get("nome")
		tipoDispositivo_id = request.form.get("tipoDpt")
		topico = request.form.get("topico")

		if name and tipoDispositivo_id and topico:
			dpts.name = name
			dpts.tipoDispositivo_id = tipoDispositivo_id
			dpts.topico = topico

			db.session.commit()
		
		return redirect(url_for("tablesDisp"))
	
	return render_template("atualizarDisp.html", dpts=dpts, dispositivo=dispositivo)

@app.route("/atualizarRelacao/<int:id>", methods=['GET', 'POST'])
def atualizarRelacao(id):
	relacao = RelacaoDispUsu.query.filter_by(id=id).first()

	if request.method == "POST":
		usuario_id = request.form.get("usuario")
		dispositivo_id = request.form.get("dispositivo")

		if usuario_id and dispositivo_id:
			relacao.usuario_id = usuario_id
			relacao.dispositivo_id = dispositivo_id

			db.session.commit()
		
		return redirect(url_for("tablesRelacio"))
	
	return render_template("atualizarRelacao.html", relacao=relacao)


@app.route("/perfil")
def perfil():

	return render_template("perfil.html")

@app.route("/tablesUsu", methods=['GET', 'POST'])
def tablesUsu():
	form = RegistrarUsu()

	if form.validate_on_submit():
		new_user = Usuario(nome=form.nome.data, email=form.email.data, senha=form.senha.data, perfil=form.perfil.data)
		#new_user = User(username=form.username.data, email=form.username.data, password=form.password.data)
		db.session.add(new_user)
		db.session.commit()
		return redirect(url_for("tablesUsu"))

	usuario = Usuario.query.all()	
	return render_template("tablesUsu.html", usuario=usuario, form=form)

@app.route("/tablesDisp", methods=['GET', 'POST'])
def tablesDisp():
	form = RegistrarDispositivo()

	if form.validate_on_submit():
		new_user = Dispositivo(tipoDispositivo_id=form.tipoDispositivo_id.data,name=form.name.data,topico=form.topico.data)
		#new_user = User(username=form.username.data, email=form.username.data, password=form.password.data)
		db.session.add(new_user)
		db.session.commit()

	dispositivo = Dispositivo.query.all()
	return render_template("tablesDisp.html", dispositivo=dispositivo, form=form)

@app.route("/tablesTiposDisp", methods=['GET', 'POST'])
def tablesTiposDisp():
	form = RegistraTipodispositivo()

	if form.validate_on_submit():
		new_user = Tipodispositivo(name=form.name.data, descricao=form.descricao.data, tipodeDado=form.tipodeDado.data)
		#new_user = User(username=form.username.data, email=form.username.data, password=form.password.data)
		db.session.add(new_user)
		db.session.commit()
		
	tipoDpt = Tipodispositivo.query.all()	
	return render_template("tablesTiposDisp.html", tipoDpt=tipoDpt, form=form)

@app.route("/tablesRelacio", methods=['GET', 'POST'])
def tablesRelacio():
	form = RegistrarRelacao()
	relacao = RelacaoDispUsu.query.all()

	if form.validate_on_submit():
		new_user = RelacaoDispUsu(usuario_id=form.usuario_id.data, dispositivo_id=form.dispositivo_id.data)
		#new_user = User(username=form.username.data, email=form.username.data, password=form.password.data)
		db.session.add(new_user)
		db.session.commit()

	#relacao = RelacaoDispUsu.query.all()	

	return render_template("tablesRelacio.html", relacao=relacao, form=form)


if __name__ == '__main__':
	#conexao
	socketio.run(app, host='0.0.0.0', port=5000, use_reloader=True, debug=True)