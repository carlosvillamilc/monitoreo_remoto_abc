import json
from unittest import TestCase

from faker import Faker
from faker.generator import random

from app import app


class TestApostador(TestCase):

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

    def test_obtener_apuestas_apostador(self):
        nueva_carrera = {
            "nombre": self.data_factory.sentence(),
            "competidores": [
                {
                    "probabilidad": 0.6,
                    "competidor": "Lorem ipsum"
                },
                {
                    "probabilidad": round(random.uniform(0.1, 0.99), 2),
                    "competidor": self.data_factory.name()
                },
                {
                    "probabilidad": round(random.uniform(0.1, 0.99), 2),
                    "competidor": self.data_factory.name()
                }
            ]
        }

        endpoint_carreras = "/usuario/{}/carreras".format(
            str(self.usuario_code))
        headers = {'Content-Type': 'application/json',
                   "Authorization": "Bearer {}".format(self.token)}

        solicitud_nueva_carrera = self.client.post(endpoint_carreras,
                                                   data=json.dumps(
                                                       nueva_carrera),
                                                   headers=headers)

        respuesta_al_crear_carrera = json.loads(
            solicitud_nueva_carrera.get_data())
        id_carrera = respuesta_al_crear_carrera["id"]
        id_competidor = \
            [x for x in respuesta_al_crear_carrera["competidores"]
                if x["nombre_competidor"] == "Lorem ipsum"][0]["id"]

        nueva_apuesta = {
            "valor_apostado": random.uniform(100, 500000),
            "id_usuario": self.usuario_code,
            "id_competidor": id_competidor,
            "id_carrera": id_carrera
        }

        endpoint_apuestas = "/apuestas"

        solicitud_nueva_apuesta = self.client.post(endpoint_apuestas,
                                                   data=json.dumps(
                                                       nueva_apuesta),
                                                   headers=headers)

        respuesta_al_crear_apuesta = json.loads(
            solicitud_nueva_apuesta.get_data())

        endpoint_apuestas_apostador = "/apuestasapostador/{}".format(
            str(self.usuario_code))

        solicitud_apuestas_apostador = self.client.get(
            endpoint_apuestas_apostador, headers=headers)
        apuestas_apostador = json.loads(
            solicitud_apuestas_apostador.get_data())

        self.assertEqual(solicitud_apuestas_apostador.status_code, 200)

    def test_obtener_apostador(self):

        headers = {'Content-Type': 'application/json',
                   "Authorization": "Bearer {}".format(self.token)}

        endpoint_apostador = "/apostadores"

        solicitud_consulta_apostadores = self.client.get(
            endpoint_apostador, headers=headers)
        total_apostadores = len(json.loads(
            solicitud_consulta_apostadores.get_data()))

        self.assertEqual(solicitud_consulta_apostadores.status_code, 200)
        #self.assertGreater(total_apuestas_despues, total_apuestas_antes)

    def test_obtener_usuario_por_id(self):
        nuevo_apostador = {
            "usuario": self.data_factory.name(),
            "contrasena": self.data_factory.word(),
            "rol": "APOSTADOR"
        }
        endpoint_apostadores = "/apostadores"
        headers = {'Content-Type': 'application/json',
                   "Authorization": "Bearer {}".format(self.token)}

        solicitud_nuevo_apostador = self.client.post(endpoint_apostadores,
                                                     data=json.dumps(
                                                         nuevo_apostador),
                                                     headers=headers)

        respuesta_al_crear_apostador = json.loads(
            solicitud_nuevo_apostador.get_data())
        id_usuario = respuesta_al_crear_apostador["id"]
        endpoint_apostadorId = "/apostador/{}".format(str(id_usuario))

        solicitud_consultar_apostador_por_id = self.client.get(
            endpoint_apostadorId, headers=headers)
        apostador_obtenido = json.loads(
            solicitud_consultar_apostador_por_id.get_data())

        self.assertEqual(solicitud_consultar_apostador_por_id.status_code, 200)

    def test_editar_apostador(self):
        endpoint_apostadores = "/apostadores"
        headers = {'Content-Type': 'application/json',
                   "Authorization": "Bearer {}".format(self.token)}

        nuevo_apostador = {
            "usuario": self.data_factory.name(),
            "contrasena": self.data_factory.word(),
            "rol": "APOSTADOR"
        }

        solicitud_nuevo_apostador = self.client.post(endpoint_apostadores,
                                                     data=json.dumps(
                                                         nuevo_apostador),
                                                     headers=headers)
        respuesta_al_crear_apostador = json.loads(
            solicitud_nuevo_apostador.get_data())
        id_apostador = respuesta_al_crear_apostador["id"]

        endpoint_apostador = "/apostador/{}".format(str(id_apostador))
        apostador_editado = {
            "usuario": "user1",
            "contrasena": "12345",
            "rol": "APOSTADOR"
        }
        solicitud_editar_apostador = self.client.put(
            endpoint_apostador, data=json.dumps(apostador_editado), headers=headers)

        respuesta_al_editar_apostador = json.loads(
            solicitud_editar_apostador.get_data())

        self.assertEqual(solicitud_editar_apostador.status_code, 200)
