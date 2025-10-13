import unittest
import os
from flask import current_app
from app import create_app
from app.models import Grado
from app.services import GradoService
from app import db
from test.instancias import nuevogrado


class GradoTestCase(unittest.TestCase):
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
        grado = nuevogrado()
        self.assertIsNotNone(grado)
        self.assertIsNotNone(grado.id)
        self.assertGreaterEqual(grado.id, 1)
        self.assertEqual(grado.nombre, "Primero")

    def test_buscar_por_id(self):
        grado = nuevogrado()
        r=GradoService.buscar_por_id(grado.id)
        self.assertIsNotNone(r)
        self.assertEqual(r.nombre, "Primero")
        self.assertEqual(r.descripcion, "Descripcion del primer grado")

    
    def test_buscar_todos(self):
        grado1 = nuevogrado()
        grado2 = nuevogrado()
        grados = GradoService.buscar_todos()
        self.assertIsNotNone(grados)
        self.assertGreaterEqual(len(grados), 2)

    def test_actualizar(self):
        grado= nuevogrado()
        grado.nombre = "Segundo"
        grado.descripcion = "Descripción del segundo grado"

    def test_borrar(self):
        universidad = nuevogrado()
        borrado = GradoService.borrar_por_id(universidad.id)
        self.assertTrue(borrado)
        resultado = GradoService.buscar_por_id(universidad.id)
        self.assertIsNone(resultado)

  