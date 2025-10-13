import unittest
import os
from flask import current_app
from app import create_app
from app.models.area import Area
from app.services import AreaService
from test.instancias import nuevaarea
from app import db

class AreaTestCase(unittest.TestCase):
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
        area = nuevaarea()
        self.assertIsNotNone(area)
        self.assertIsNotNone(area.id)
        self.assertGreaterEqual(area.id, 1)
        self.assertEqual(area.nombre, "Matematica")

    def test_buscar_por_id(self):
        area = nuevaarea()
        r = AreaService.buscar_por_id(area.id)
        self.assertIsNotNone(r)
        self.assertEqual(r.nombre, "Matematica")

    def test_buscar_todos(self):
        area1 = nuevaarea("Matematica")
        area2 = nuevaarea("nombre2")
        areas = AreaService.buscar_todos()
        self.assertIsNotNone(areas)
        self.assertEqual(len(areas), 2)

    def test_actualizar(self):
        area = nuevaarea()
        area.nombre = "nombre actualizado"
        area_actualizado = AreaService.actualizar(area.id, area)
        self.assertEqual(area_actualizado.nombre, "nombre actualizado")

    def test_borrar(self):
        area = nuevaarea()
        borrado= AreaService.borrar_por_id(area.id)
        self.assertTrue(borrado)
        resultado = AreaService.buscar_por_id(area.id)
        self.assertIsNone(resultado)
