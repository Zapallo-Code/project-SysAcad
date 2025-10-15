from django.test import TestCase
from app.models import Orientation
from app.services import OrientationService
from tests.fixtures import new_orientation
from datetime import date



class OrientationTestCase(TestCase):

    def test_crear(self):
        orientation = new_orientation()
        self.assertIsNotNone(orientation)
        self.assertIsNotNone(orientation.name)
        self.assertGreaterEqual(orientation.name, "Orientation 1")
        self.assertEqual(orientation.specialty.specialty_type.name, "Cardiology")
        self.assertEqual(orientation.plan.start_date, date(2024, 6, 4))
        self.assertIsNotNone(orientation.subject.name, "Development")

    def test_find_by_id(self):
        orientation = new_orientation()
        r = OrientationService.find_by_id(orientation.id)
        self.assertIsNotNone(r)
        self.assertEqual(r.name, "Orientation 1")

    def test_buscar_todos(self):
        orientation1 = new_orientation()
        orientation2 = new_orientation(name="Orientation B")

        orientations = OrientationService.find_all()
        self.assertIsNotNone(orientations)
        self.assertGreaterEqual(len(orientations), 2)

    def test_actualizar(self):
        orientation = new_orientation()
        orientation.name = "Orientation Actualizada"
        orientation_actualizada = OrientationService.update(orientation.id, orientation)
        self.assertEqual(orientation_actualizada.name, "Orientation Actualizada")

    def test_borrar(self):
        orientation = new_orientation()
        borrado = OrientationService.delete_by_id(orientation.id)
        self.assertTrue(borrado)
        resultado = OrientationService.find_by_id(orientation.id)
        self.assertIsNone(resultado)





