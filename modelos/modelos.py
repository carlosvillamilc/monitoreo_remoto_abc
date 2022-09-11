from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import enum

db = SQLAlchemy()


class Central(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    direccion = db.Column(db.String(128))
    sede = db.Column(db.String(128))
    operario = db.Column(db.String(128))


class CentralSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Central
