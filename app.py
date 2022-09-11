from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from modelos import db
from vistas import VistaEvento, VistaEventos, VistaUbicacion, VistaUbicaciones, VistaUsuario, VistaUsuarios
from vistas import VistaUbicacionByidUsuario, VistaEventoByidUsuario

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MSCon.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
api.add_resource(VistaEvento, '/eventos/<int:id_evento>')
api.add_resource(VistaEventoByidUsuario, '/eventosbyidusuario/<int:id_usuario>')
api.add_resource(VistaEventos, '/eventos')
api.add_resource(VistaUbicacion, '/ubicacion/<int:id_ubicacion>')
api.add_resource(VistaUbicacionByidUsuario, '/ubicacionbyidusuario/<int:id_usuario>')
api.add_resource(VistaUbicaciones, '/ubicaciones')
api.add_resource(VistaUsuario, '/usuarios/<int:id_usuario>')
api.add_resource(VistaUsuarios, '/usuarios')

jwt = JWTManager(app)
