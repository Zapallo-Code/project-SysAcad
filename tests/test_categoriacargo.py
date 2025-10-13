import unittest
import os
from flask import current_app
from app import create_app
from app.models.categoriacargo import CategoriaCargo
from app.services import CategoriaCargoService
from test.instancias import nuevacategoriacargo
from app import db

class CategoriaCargoTestCase(unittest.TestCase):
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
        categoria = nuevacategoriacargo()
        self.assertIsNotNone(categoria)
        self.assertIsNotNone(categoria.id)
        self.assertGreaterEqual(categoria.id, 1)
        self.assertEqual(categoria.nombre, "Docente")

    def test_buscar_por_id(self):
        categoria = nuevacategoriacargo()
        r=CategoriaCargoService.buscar_por_id(categoria.id)
        self.assertIsNotNone(r)
        self.assertEqual(r.nombre, "Docente")
        
    
    def test_buscar_todos(self):
        categoria1 = nuevacategoriacargo()
        categoria2 = nuevacategoriacargo()
        categorias = CategoriaCargoService.buscar_todos()
        self.assertIsNotNone(categorias)
        self.assertEqual(len(categorias), 2)

    def test_actualizar(self):
        categoria = nuevacategoriacargo()
        categoria.nombre = "Docente actualizado"
        categoria_actualizado = CategoriaCargoService.actualizar(categoria.id, categoria)
        self.assertEqual(categoria_actualizado.nombre, "Docente actualizado")

    def test_borrar(self):
        categoria = nuevacategoriacargo()
        borrado= CategoriaCargoService.borrar_por_id(categoria.id)
        self.assertTrue(borrado)
        resultado = CategoriaCargoService.buscar_por_id(categoria.id)
        self.assertIsNone(resultado)

    
        