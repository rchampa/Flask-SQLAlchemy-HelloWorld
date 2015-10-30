__author__ = 'Ricardo'

from myJson import to_json
from application import db
import datetime


class Usuario(db.Model):
  __tablename__ = 'usuarios'
  id_usuario = db.Column(db.Integer, primary_key = True)
  telefono = db.Column(db.String(12))
  email = db.Column(db.String(64))
  genero = db.Column(db.Integer)
  nombre = db.Column(db.String(30))
  apellidos = db.Column(db.String(30))
  edad = db.Column(db.Integer)
  borrado = db.Column(db.Boolean)
  creado_en = db.Column(db.DateTime)
  actualizado_en = db.Column(db.DateTime)
  ultima_conexion = db.Column(db.DateTime)
  #fotos

  def __init__(self, telefono, email, genero, nombre, apellidos, edad):
    self.telefono = telefono
    self.email = email
    self.genero = genero
    self.nombre = nombre
    self.apellidos = apellidos
    self.edad = edad
    self.borrado = False
    self.creado_en = datetime.datetime.utcnow()

  @property
  def json(self):
    return to_json(self, self.__class__)



class Foto(db.Model):
  __tablename__ = 'fotos'
  id_foto = db.Column(db.Integer, primary_key = True)
  id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'))
  num_likes = db.Column(db.Integer)
  publica = db.Column(db.Boolean)
  borrado = db.Column(db.Boolean)
  url = db.Column(db.Text)
  creado_en = db.Column(db.DateTime)
  actualizado_en = db.Column(db.DateTime)
  usuario = db.relationship('Usuario', backref=db.backref('fotos', lazy='dynamic'))
  #comentarios

  def __init__(self, usuario, publica, url):
    self.usuario = usuario
    self.num_likes = 0
    self.publica = publica
    self.url = url
    self.borrado = False
    self.creado_en = datetime.datetime.utcnow()

  @property
  def json(self):
    return to_json(self, self.__class__)