import unittest
import os
from flask import current_app
from app import create_app
from app.models.plan import Plan
from app.services import PlanService
from test.instancias import nuevoplan
from app import db
from datetime import date



class PlanTestCase(unittest.TestCase):
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
        plan = nuevoplan()
        self.assertIsNotNone(plan)
        self.assertIsNotNone(plan.id)
        self.assertGreaterEqual(plan.id, 1)
        self.assertEqual(plan.nombre, "Plan A")

    def test_buscar_por_id(self):
        plan = nuevoplan()
        r = PlanService.buscar_por_id(plan.id)
        self.assertIsNotNone(r)
        self.assertEqual(r.nombre, plan.nombre)
        self.assertEqual(r.fecha_inicio, plan.fecha_inicio)
        self.assertEqual(r.fecha_fin, plan.fecha_fin)
        self.assertEqual(r.observacion, plan.observacion)

    def test_buscar_todos(self):
        plan1 = nuevoplan()
        plan2 = nuevoplan("Plan B", date(2024, 7, 4), date(2024, 8, 4), "Observacion de prueba 2")
        planes = PlanService.buscar_todos()
        self.assertIsNotNone(planes)
        self.assertEqual(len(planes), 2)

    def test_actualizar(self):
        plan = nuevoplan()
        plan.nombre = "Plan Actualizado"
        plan_actualizado = PlanService.actualizar(plan.id, plan)
        self.assertEqual(plan_actualizado.nombre, "Plan Actualizado")

    def test_borrar_por_id(self):
        plan = nuevoplan()
        borrado = PlanService.borrar_por_id(plan.id)
        self.assertTrue(borrado)
        r = PlanService.buscar_por_id(plan.id)
        self.assertIsNone(r)

