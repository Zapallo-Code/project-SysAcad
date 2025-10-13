import unittest
import os
from flask import current_app
from app import create_app
from app.models.tipodedicacion import TipoDedicacion
from app.services import TipoDedicacionService
from app import db
from test.instancias import nuevotipodedicacion

class TipoDedicacionTestCase(unittest.TestCase):
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
        tipodedicacion = nuevotipodedicacion()
        self.assertIsNotNone(tipodedicacion)
        self.assertIsNotNone(tipodedicacion.id)
        self.assertGreaterEqual(tipodedicacion.id,1)
        self.assertEqual(tipodedicacion.nombre, "Dedicacion Completa")
        self.assertEqual(tipodedicacion.observacion, "Observacion de prueba")

    def test_buscar_por_id(self):
        tipodedicacion = nuevotipodedicacion()
        r=TipoDedicacionService.buscar_por_id(tipodedicacion.id)
        self.assertIsNotNone(r)
        self.assertEqual(r.nombre, "Dedicacion Completa")
        self.assertEqual(r.observacion, "Observacion de prueba")
    
    def test_buscar_todos(self):
        tipodedicacion1 = nuevotipodedicacion()
        tipodedicacion2 = nuevotipodedicacion("Dedicacion Completa 2", "Observacion de prueba 2")
        dedicaciones = TipoDedicacionService.buscar_todos()
        self.assertIsNotNone(dedicaciones)
        self.assertEqual(len(dedicaciones), 2)

    def test_actualizar(self):
        tipodedicacion = nuevotipodedicacion()
        tipodedicacion.nombre = "Dedicacion actualizada"
        tipodededicacion_actualizado = TipoDedicacionService.actualizar(tipodedicacion.id ,tipodedicacion)
        self.assertEqual(tipodededicacion_actualizado.nombre, "Dedicacion actualizada")

    def test_borrar(self):
        tipodedicacion = nuevotipodedicacion()
        borrado = TipoDedicacionService.borrar_por_id(tipodedicacion.id)
        self.assertTrue(borrado)
        resultado = TipoDedicacionService.buscar_por_id(tipodedicacion.id)
        self.assertIsNone(resultado)

    