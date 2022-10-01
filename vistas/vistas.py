from ast import Break
from unittest import result
from flask import request
from flask_jwt_extended import jwt_required, create_access_token, decode_token, get_jwt
from flask_restful import Resource
from sqlalchemy import false, null
from sqlalchemy.exc import IntegrityError
import jwt
import json
import time
from datetime import datetime, timedelta, timezone

from modelos import db, Central, Usuario, UsuarioSchema, CentralSchema, TokenRevocado

central_schema = CentralSchema()
usuario_schema = UsuarioSchema()

key='super-secret'
expires_token=6000

class VistaSignIn(Resource):

    def post(self):
        nuevo_usuario = Usuario(usuario=request.json["usuario"],
                                contrasena=request.json["contrasena"],
                                tipo_usuario=request.json["tipo_usuario"],
                                email=request.json["email"])
        db.session.add(nuevo_usuario)
        db.session.commit()
        dt = datetime.now(tz=timezone.utc) + timedelta(seconds=expires_token)
        payload={"usuario":nuevo_usuario.usuario,"contrasena":nuevo_usuario.contrasena,"exp":dt}
        token_de_acceso = jwt.encode(payload, key,algorithm="HS256")
        #token_de_acceso = create_access_token(identity=nuevo_usuario.id)
        return {"mensaje": "usuario creado exitosamente", "token": token_de_acceso, "expiracion_token":dt.strftime("%d/%m/%Y, %H:%M:%S"),"id": nuevo_usuario.id}        

    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.contrasena = request.json.get("contrasena", usuario.contrasena)
        db.session.commit()
        return usuario_schema.dump(usuario)

    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204


class VistaLogIn(Resource):

    def post(self):
        usuario = Usuario.query.filter(Usuario.usuario == request.json["usuario"],
                                       Usuario.contrasena == request.json["contrasena"]).first()
        db.session.commit()
        if usuario is None:
            return "El usuario no existe", 404
        else:
            #token_de_acceso = create_access_token(identity=usuario.id)
            dt = datetime.now(tz=timezone.utc) + timedelta(seconds=expires_token)
            print(dt)            
            payload={"usuario":usuario.usuario,"contrasena":usuario.contrasena,"exp":dt}
            token_de_acceso = jwt.encode(payload, key,algorithm="HS256")
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso, "expiracion":dt.strftime("%d/%m/%Y, %H:%M:%S")}


class VistaValidateToken(Resource):
    
    def post(self):
        try:                
            token = request.headers["Authorization"]
        except:
            return {"Error": "Sin token autenticación"}, 405
            
        token = token.replace('Bearer ','')
        
        #token=request.json["token"]
        contrasena_body=request.json["contrasena"]
        try:
        
            decoded_data = jwt.decode(token, key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            # Signature has expired            
            return {"Error": "Token Expirado"}, 405
        
        #usuario = decoded_data["usuario"]
        contrasena = decoded_data["contrasena"]
        
        if contrasena != contrasena_body:
            nuevo_token_revocado = TokenRevocado(tokenr = token)
            db.session.add(nuevo_token_revocado)
            db.session.commit()
            return {"Error": "Error confirmación contraseña"}, 405
        
        
        tokenBd = TokenRevocado.query.filter(TokenRevocado.tokenr == token).first()
        db.session.commit()
        if tokenBd is None:
            return {"Respuesta": "Credenciales y token validadas"},200
        else:
            return {"Error": "Token Revocado"}, 405
