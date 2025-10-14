from django.test import TestCase
from app.models import Orientation
from app.services import OrientationService
from tests.instancias import new_orientation
from datetime import date



class OrientationTestCase(TestCase):

    def test_crear(self):
        orientacion = new_orientation()
        self.assertIsNotNone(orientacion)
        self.assertIsNotNone(orientacion.name)
        self.assertGreaterEqual(orientacion.name, "Orientation 1")
        self.assertEqual(orientacion.specialty.specialty_type.name, "Cardiologia")
        self.assertEqual(orientacion.plan.start_date, date(2024, 6, 4))
        self.assertIsNotNone(orientacion.subject.name, "Desarrollo")

    def test_find_by_id(self):
        orientacion = new_orientation()
        r = OrientationService.find_by_id(orientacion.id)
        self.assertIsNotNone(r)
        self.assertEqual(r.name, "Orientation 1")

    def test_buscar_todos(self):
        orientacion1 = new_orientation()
        orientacion2 = new_orientation(name="Orientation B")

        orientations = OrientationService.find_all()
        self.assertIsNotNone(orientations)
        self.assertGreaterEqual(len(orientations), 2)

    def test_actualizar(self):
        orientacion = new_orientation()
        orientacion.name = "Orientation Actualizada"
        orientacion_actualizada = OrientationService.update(orientacion.id, orientacion)
        self.assertEqual(orientacion_actualizada.name, "Orientation Actualizada")

    def test_borrar(self):
        orientacion = new_orientation()
        borrado = OrientationService.delete_by_id(orientacion.id)
        self.assertTrue(borrado)
        resultado = OrientationService.find_by_id(orientacion.id)
        self.assertIsNone(resultado)





