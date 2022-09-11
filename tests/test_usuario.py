import json
from unicodedata import name
from unittest import TestCase

from faker import Faker
from faker.generator import random

from app import app

class TestUsuario(TestCase):
    
    def setUp(self):
        self.data_factory = Faker()
        self.client = app.test_client()

        nuevo_usuario = {
            "usuario": self.data_factory.name(),
            "contrasena": self.data_factory.word(),
            "rol": "APOSTADOR"
        }

        solicitud_nuevo_usuario = self.client.post("/signin",
                                                   data=json.dumps(nuevo_usuario),
                                                   headers={'Content-Type': 'application/json'})

        respuesta_al_crear_usuario = json.loads(solicitud_nuevo_usuario.get_data())

        self.token = respuesta_al_crear_usuario["token"]
        self.usuario_code = respuesta_al_crear_usuario["id"]
        
    def test_obtener_usuario_por_id(self):
        nuevo_apostador = {
            "usuario": self.data_factory.name(), 
            "contrasena": self.data_factory.word(), 
            "rol": "APOSTADOR"
        }
        endpoint_apostadores = "/apostadores"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}

        solicitud_nuevo_apostador = self.client.post(endpoint_apostadores,
                                                   data=json.dumps(nuevo_apostador),
                                                   headers=headers)

        respuesta_al_crear_apostador = json.loads(solicitud_nuevo_apostador.get_data())
        id_usuario = respuesta_al_crear_apostador["id"]
        endpoint_apostadorId = "/apostador/{}".format(str(id_usuario))

        solicitud_consultar_apostador_por_id = self.client.get(endpoint_apostadorId, headers=headers)
        apostador_obtenido = json.loads(solicitud_consultar_apostador_por_id.get_data())

        self.assertEqual(solicitud_consultar_apostador_por_id.status_code, 200)

def test_editar_apostador(self):
        endpoint_apostadores = "/apostadores"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(self.token)}
        
        nuevo_apostador = {
            "usuario": self.data_factory.name(), 
            "contrasena": self.data_factory.word(), 
            "rol": "APOSTADOR"
        }
        
        solicitud_nuevo_apostador = self.client.post(endpoint_apostadores,
                                                   data=json.dumps(nuevo_apostador),
                                                   headers=headers)
        respuesta_al_crear_apostador = json.loads(solicitud_nuevo_apostador.get_data())
        nombre_apostador_antes = respuesta_al_crear_apostador["usuario"]
        id_apostador = respuesta_al_crear_apostador["id"]

        endpoint_apostador = "/apostador/{}".format(str(id_apostador))
        apostador_editado = {
            "usuario": "user1", 
            "contrasena": "12345",
            "rol": "APOSTADOR"
        }
        solicitud_editar_apostador = self.client.put(endpoint_apostador, data=json.dumps(apostador_editado), headers=headers)

        respuesta_al_editar_apostador = json.loads(solicitud_editar_apostador.get_data())
        nombre_apostador_despues = respuesta_al_editar_apostador["usuario"]

        self.assertEqual(solicitud_editar_apostador.status_code, 200)
        self.assertNotEqual(nombre_apostador_antes, nombre_apostador_despues)
        
