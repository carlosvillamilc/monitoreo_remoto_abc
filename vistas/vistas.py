from ast import Break
from unittest import result
from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource
import requests
import json

from modelos import db, Central, CentralSchema

central_schema = CentralSchema()


class VistaCentral(Resource):

    # @jwt_required()
    def post(self):
        direccion = request.json["direccion"]
        sede = request.json["sede"]
        operario = request.json["operario"]
        contrasena = request.json["contrasena"]
        token = request.headers['Authorization']

        parameter_token = token.replace("Bearer", "").strip()
        #print("Contraseña: " + contrasena)
        #print("Token: " + parameter_token)

        api_url = "http://127.0.0.1:5000/checktoken"

        payload = json.dumps({"contrasena": contrasena})

        headers = {'Authorization': 'Bearer {}'.format(
            parameter_token), 'Content-Type': 'application/json'}

        response = requests.request(
            "POST", api_url, headers=headers, data=payload)

        #print("Codigo respuesta: " + str(response.status_code))

        if (response.status_code == 200):
            nueva_central = Central(direccion=direccion,
                                    sede=sede,
                                    operario=operario)

            db.session.add(nueva_central)
            db.session.commit()
            return central_schema.dump(nueva_central)
        else:
            return {"Error": "Transacción Invalidada"}, 405
