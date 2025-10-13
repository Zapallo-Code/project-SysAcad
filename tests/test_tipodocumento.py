import unittest
import os
from flask import current_app
from app import create_app
from app.models.tipodocumento import TipoDocumento
from app.services import TipoDocumentoService
from test.instancias import nuevotipodocumento
from app import db

class TipoDocumentoTestCase(unittest.TestCase):
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
        tipodocumento = nuevotipodocumento()
        self.assertIsNotNone(tipodocumento)
        self.assertIsNotNone(tipodocumento.id)
        self.assertGreaterEqual(tipodocumento.id, 1)
        self.assertEqual(tipodocumento.dni, 46291002)

    def test_buscar_por_id(self):
        tipodocumento = nuevotipodocumento()
        r=TipoDocumentoService.buscar_por_id(tipodocumento.id)
        self.assertIsNotNone(r)
        self.assertEqual(r.dni, 46291002)
        self.assertEqual(r.libreta_civica, "nacional")

    def test_buscar_todos(self):
        tipodocumento1 = nuevotipodocumento()
        tipodocumento2 = nuevotipodocumento(48291002, "23456789", "98765432", "CD123456")
        documentos = TipoDocumentoService.buscar_todos()
        self.assertIsNotNone(documentos)
        self.assertEqual(len(documentos), 2)

    def test_actualizar(self):
        tipodocumento = nuevotipodocumento()
        tipodocumento.dni = 89291002
        tipodocumento_actualizado = TipoDocumentoService.actualizar(tipodocumento.id, tipodocumento)
        self.assertEqual(tipodocumento_actualizado.dni, 89291002)
    
    def test_borrar(self):
        tipodocumento = nuevotipodocumento()
        borrado = TipoDocumentoService.borrar_por_id(tipodocumento.id)
        self.assertTrue(borrado)
        resultado = TipoDocumentoService.buscar_por_id(tipodocumento.id)
        self.assertIsNone(resultado)
