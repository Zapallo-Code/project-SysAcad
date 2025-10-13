import unittest
import os
from flask import current_app
from app import create_app
from app.models import Universidad
from app.services import UniversidadService
from app import db
from test.instancias import nuevauniversidad

class UniversidadTestCase(unittest.TestCase):
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
        universidad = nuevauniversidad()
        self.assertIsNotNone(universidad)
        self.assertIsNotNone(universidad.id)
        self.assertGreaterEqual(universidad.id, 1)
        self.assertEqual(universidad.nombre, "Universidad Nacional")

    def test_buscar_por_id(self):
        universidad = nuevauniversidad()
        r=UniversidadService.buscar_por_id(universidad.id)
        self.assertIsNotNone(r)
        self.assertEqual(r.nombre, "Universidad Nacional")
        self.assertEqual(r.sigla, "UN")
    
    def test_buscar_todos(self):
        universidad1 = nuevauniversidad()
        universidad2 = nuevauniversidad()
        universidades = UniversidadService.buscar_todos()
        self.assertIsNotNone(universidades)
        self.assertEqual(len(universidades), 2)

    def test_actualizar(self):
        universidad = nuevauniversidad()
        universidad.nombre = "Universidad Actualizada"
        universidad_actualizada = UniversidadService.actualizar(universidad.id,universidad)
        self.assertEqual(universidad_actualizada.nombre, "Universidad Actualizada")

    def test_borrar(self):
        universidad = nuevauniversidad()
        borrado = UniversidadService.borrar_por_id(universidad.id)
        self.assertTrue(borrado)
        resultado = UniversidadService.buscar_por_id(universidad.id)
        self.assertIsNone(resultado)
