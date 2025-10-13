import unittest
import os
from flask import current_app
from app import create_app
from app.models import Especialidad, TipoEspecialidad
from app.services import EspecialidadService, TipoEspecialidadService
from test.instancias import nuevaespecialidad, nuevotipoespecialidad
from app import db

class EspecialidadTestCase(unittest.TestCase):
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
        especialidad= nuevaespecialidad()
        self.assertIsNotNone(especialidad)
        self.assertIsNotNone(especialidad.id)
        self.assertGreaterEqual(especialidad.id,1)
        self.assertEqual(especialidad.nombre, "Matematicas")
        self.assertEqual(especialidad.tipoespecialidad.nombre, "Cardiologia")

    def test_buscar_por_id(self):
        especialidad = nuevaespecialidad()
        r=EspecialidadService.buscar_por_id(especialidad.id)
        self.assertIsNotNone(r)
        self.assertEqual(r.nombre, "Matematicas")
        self.assertEqual(r.letra, "A")

    def test_buscar_todos(self):
        especialidad1 =nuevaespecialidad()
        especialidad2 =nuevaespecialidad()
        especialidades = EspecialidadService.buscar_todos()
        self.assertIsNotNone(especialidades)
        self.assertEqual(len(especialidades),2)

    def test_actualizar(self):
        especialidad = nuevaespecialidad()
        especialidad.nombre = "matematica actualizada"
        especialidad_actualizada = EspecialidadService.actualizar(especialidad.id, especialidad)
        self.assertEqual(especialidad_actualizada.nombre, "matematica actualizada")

    def test_borrar(self):
        especialidad = nuevaespecialidad()
        borrado = EspecialidadService.borrar_por_id(especialidad.id)
        self.assertTrue(borrado)
        resultado = EspecialidadService.buscar_por_id(especialidad.id)
        self.assertIsNone(resultado)

    