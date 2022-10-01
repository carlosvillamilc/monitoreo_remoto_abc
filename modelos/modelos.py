from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import enum

db = SQLAlchemy()

@enum.unique            
class TipoUsuario(int, enum.Enum):
    CLIENTE: int = 1                                      
    OPERADOR: int = 2
    ADMINISTRADOR: int = 3


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))
    tipo_usuario = db.Column(db.Enum(TipoUsuario))
    email = db.Column(db.String(50))
    

class Central(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    direccion = db.Column(db.String(128))
    sede = db.Column(db.String(128))
    operario = db.Column(db.String(128))
    
    
class TokenRevocado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tokenr = db.Column(db.String())


class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        include_fk = True
        load_instance = True


class CentralSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Central
