import unittest
import os
from flask import current_app
from app import create_app
from app.models import Orientacion
from app.services import OrientacionService
from test.instancias import nuevaorientacion
from app import db
from datetime import date



class OrientacionTestCase(unittest.TestCase):
    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_crear(self):
        orientacion = nuevaorientacion()
        self.assertIsNotNone(orientacion)
        self.assertIsNotNone(orientacion.nombre)
        self.assertGreaterEqual(orientacion.nombre, "Orientacion 1")
        self.assertEqual(orientacion.especialidad.tipoespecialidad.nombre, "Cardiologia")
        self.assertEqual(orientacion.plan.fecha_inicio, date(2024,6,4))
        self.assertIsNotNone(orientacion.materia.nombre, "Desarrollo")

    def test_buscar_por_id(self):
        orientacion = nuevaorientacion()
        r=OrientacionService.buscar_por_id(orientacion.id)
        self.assertIsNotNone(r)
        self.assertEqual(r.nombre, "Orientacion 1")

    def test_buscar_todos(self):
        orientacion1 = nuevaorientacion()
        orientacion2 = nuevaorientacion(nombre="Orientacion B")

        orientaciones = OrientacionService.buscar_todos()
        self.assertIsNotNone(orientaciones)
        self.assertGreaterEqual(len(orientaciones), 2)

    def test_actualizar(self):
        orientacion = nuevaorientacion()
        orientacion.nombre = "Orientacion Actualizada"
        orientacion_actualizada = OrientacionService.actualizar(orientacion.id, orientacion)
        self.assertEqual(orientacion_actualizada.nombre, "Orientacion Actualizada")

    def test_borrar(self):
        orientacion = nuevaorientacion()
        borrado = OrientacionService.borrar_por_id(orientacion.id)
        self.assertTrue(borrado)
        resultado = OrientacionService.buscar_por_id(orientacion.id)
        self.assertIsNone(resultado)





