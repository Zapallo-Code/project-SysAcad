from django.test import TestCase
from app.models.plan import Plan
from app.services import PlanService
from tests.fixtures import new_plan
from datetime import date



class PlanTestCase(TestCase):

    def test_crear(self):
        plan = new_plan()
        self.assertIsNotNone(plan)
        self.assertIsNotNone(plan.id)
        self.assertGreaterEqual(plan.id, 1)
        self.assertEqual(plan.name, "Plan A")

    def test_find_by_id(self):
        plan = new_plan()
        r = PlanService.find_by_id(plan.id)
        self.assertIsNotNone(r)
        self.assertEqual(r.name, plan.name)
        self.assertEqual(r.start_date, plan.start_date)
        self.assertEqual(r.end_date, plan.end_date)
        self.assertEqual(r.observation, plan.observation)

    def test_buscar_todos(self):
        plan1 = new_plan()
        plan2 = new_plan("Plan B", date(2024, 7, 4), date(2024, 8, 4), "Test observation 2")
        planes = PlanService.find_all()
        self.assertIsNotNone(planes)
        self.assertEqual(len(planes), 2)

    def test_actualizar(self):
        plan = new_plan()
        plan.name = "Updated Plan"
        plan_actualizado = PlanService.update(plan.id, plan)
        self.assertEqual(plan_actualizado.name, "Updated Plan")

    def test_borrar_por_id(self):
        plan = new_plan()
        borrado = PlanService.delete_by_id(plan.id)
        self.assertTrue(borrado)
        r = PlanService.find_by_id(plan.id)
        self.assertIsNone(r)

