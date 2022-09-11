from ast import Break
from unittest import result
from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
import json

from modelos import db, Central, CentralSchema

central_schema = CentralSchema()


class VistaApuestas(Resource):

    def post(self):
        direccion = request.json["direccion"]
        sede = request.json["sede"]
        operario = request.json["operario"]
        print("llego")
        nueva_central = Central(direccion=request.json["direccion"],
                                sede=request.json["sede"],
                                operario=request.json["operario"])

        db.session.add(nueva_central)
        db.session.commit()
        return central_schema.dump(nueva_central)
