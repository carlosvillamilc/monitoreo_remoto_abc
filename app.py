from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_mail import Mail, Message

from modelos import db
from vistas import VistaLogIn, VistaSignIn, VistaValidateToken, VistaEnviarCorreo

app = Flask(__name__)

app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'pruebaui221@gmail.com'
app.config["MAIL_PASSWORD"] = 'qbbmpiymklnjmafs'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///central.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
mail = Mail(app)
VistaEnviarCorreo.mail = mail

api.add_resource(VistaSignIn, '/signin')
api.add_resource(VistaLogIn, '/login')
api.add_resource(VistaValidateToken,'/checktoken')
api.add_resource(VistaEnviarCorreo,'/correo')

jwt = JWTManager(app)
