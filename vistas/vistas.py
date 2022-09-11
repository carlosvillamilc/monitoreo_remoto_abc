from ast import Break
from unittest import result
from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
import json

from modelos import db, Usuario, UsuarioSchema, EventosSchema, UbicacionSchema
from modelos.modelos import Eventos, Ubicacion

eventos_schema = EventosSchema()
ubicacion_schema = UbicacionSchema()
usuario_schema = UsuarioSchema()


class VistaEvento(Resource):
    def get(self, id_evento):
        return eventos_schema.dump(Eventos.query.get_or_404(id_evento))

class VistaEventoByidUsuario(Resource):
    def get(self, id_usuario):
        results = [eventos_schema.dump(evt) for evt in Eventos.query.filter(
            Eventos.usuario == id_usuario).all()]
        return results

class VistaEventos(Resource):
    def get(self):
        return [eventos_schema.dump(ca) for ca in Eventos.query.all()]

class VistaUbicacion(Resource):
    def get(self, id_ubicacion):
        return ubicacion_schema.dump(Ubicacion.query.get_or_404(id_ubicacion))

class VistaUbicacionByidUsuario(Resource):
    def get(self, id_usuario):
        results = [ubicacion_schema.dump(ubi) for ubi in Ubicacion.query.filter(
            Ubicacion.usuario == id_usuario).all()]
        return results

class VistaUbicaciones(Resource):
    def get(self):
        return [ubicacion_schema.dump(ca) for ca in Ubicacion.query.all()]

class VistaUsuario(Resource):
    def get(self, id_usuario):
        return usuario_schema.dump(Usuario.query.get_or_404(id_usuario))
        
class VistaUsuarios(Resource):
    def get(self):
        return [usuario_schema.dump(ca) for ca in Usuario.query.all()]