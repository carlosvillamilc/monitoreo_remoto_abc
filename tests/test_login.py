import json
from unittest import TestCase

from faker import Faker
from faker.generator import random

from app import app


class TestSignIn(TestCase):

    def setUp(self):
        self.data_factory = Faker()
        self.client = app.test_client()

        nuevo_usuario = {
            "usuario": self.data_factory.name(),
            "contrasena": self.data_factory.word(),
            "rol": "APOSTADOR"
        }

        solicitud_nuevo_usuario = self.client.post("/signin",
                                                   data=json.dumps(
                                                       nuevo_usuario),
                                                   headers={'Content-Type': 'application/json'})

        respuesta_al_crear_usuario = json.loads(
            solicitud_nuevo_usuario.get_data())

        self.token = respuesta_al_crear_usuario["token"]
        self.usuario_code = respuesta_al_crear_usuario["id"]

    def test_login_usuario(self):
        login = {
            "usuario": "admin",
            "contrasena": "admin"
        }

        solicitud_login_usuario = self.client.post("/login",
                                                   data=json.dumps(
                                                       login),
                                                   headers={'Content-Type': 'application/json'})

        respuesta_login_usuario = json.loads(
            solicitud_login_usuario.get_data())
        mensaje_respuesta = respuesta_login_usuario["mensaje"]

        self.assertEqual(solicitud_login_usuario.status_code, 200)
        self.assertEqual(mensaje_respuesta, "Inicio de sesión exitoso")
