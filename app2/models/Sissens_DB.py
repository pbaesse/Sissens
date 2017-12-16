from app import db

class Usuario(db.Model):
	__tablename__ = "Usuario"

	id_User = db.Column(db.Integer, primary_key=True) 
	nome = db.Column(db.String(80))
	perfil = db.Column(db.String(120))
	senha = db.Column(db.String(20))
	email = db.Column(db.String(70))

	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False

	def get_id(self):
		return str(self.id_User)
		

	def __init__(self, nome, perfil, senha, email):
		self.nome = nome
		self.perfil = perfil
		self.senha = senha
		self.email = email

	def __repr__(self):
		return "<Usuario %r>" % self.nome


class Tipos_Dpts(db.Model):
	__tablename__ = "Tipos_Dpts"

	Tipo_Dpt_id = db.Column(db.Integer, primary_key=True)
	nome_Tipo_Dpt = db.Column(db.String(40))
	descricao = db.Column(db.Text)
	topicos = db.Column(db.String(60))

	def __init__(self,nome_Tipo_Dpt, descricao, topicos):
		self.nome_Tipo_Dpt = nome_Tipo_Dpt
		self.descricao = descricao
		self.topicos = topicos

	def __repr__(self):
		return "<Tipos_Dpt %r>" % self.Tipo_Dpt_id

class Dispositivos(db.Model):	
	__tablename__ = "Dispositivos"

	id_Dpt = db.Column(db.Integer, primary_key=True)
	tipo_dpt_Id = db.Column(db.Integer, db.ForeignKey("Tipos_Dpts.Tipo_Dpt_id"))
	nome_Dpt = db.Column(db.String(30))
	URL_Foto_Dpt = db.Column(db.String)

	dpt = db.relationship('Tipos_Dpts', foreign_keys=tipo_dpt_Id)

	def __init__(self, tipo_dpt_Id, nome_Dpt, URL_Foto_Dpt):
		self.tipo_dpt_Id = tipo_dpt_Id
		self.nome_Dpt = nome_Dpt
		self.URL_Foto_Dpt = URL_Foto_Dpt

	def __repr__(self):
		return "<Dispositivos %r>" % self.id_Dpt


class Dados_Dpt(db.Model):	
	__tablename__ = "Dados_Dpt"

	id_Dados_Dpt = db.Column(db.Integer, primary_key=True)
	status_Dpt = db.Column(db.Boolean)
	nivel_Tensao = db.Column(db.Float)
	

	def __init__(self, status_Dpt,nivel_Tensao):
		self.status_Dpt = status_Dpt
		self.nivel_Tensao = nivel_Tensao

	def __repr__(self):
		return "<Dados_Dpt %r>" % self.id_Dados_Dpt
		
