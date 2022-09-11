from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import enum

db = SQLAlchemy()


class Eventos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_evento = db.Column(db.String(128))
    tipo = db.Column(db.Integer)
    ubicacion = db.Column(db.Integer, db.ForeignKey('ubicacion.id'))
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))


class Ubicacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_ubicacion = db.Column(db.String(128))
    estado = db.Column(db.Boolean, default=True)
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))


class EventosSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Eventos
        include_relationships = True
        include_fk = True
        load_instance = True


class UbicacionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Ubicacion
        include_relationships = True
        load_instance = True
        include_fk = True


class UsuarioSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True

