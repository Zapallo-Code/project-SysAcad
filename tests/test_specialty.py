from django.test import TestCase
from app.models import Specialty, SpecialtyType
from app.services import SpecialtyService, SpecialtyTypeService
from tests.fixtures import new_specialty, new_specialty_type

class SpecialtyTestCase(TestCase):

    def test_crear(self):
        specialty = new_specialty()
        self.assertIsNotNone(specialty)
        self.assertIsNotNone(specialty.id)
        self.assertGreaterEqual(specialty.id, 1)
        self.assertEqual(specialty.name, "Mathematics")
        self.assertEqual(specialty.specialty_type.name, "Cardiology")

    def test_find_by_id(self):
        specialty = new_specialty()
        r = SpecialtyService.find_by_id(specialty.id)
        self.assertIsNotNone(r)
        self.assertEqual(r.name, "Mathematics")
        self.assertEqual(r.letter, "A")

    def test_buscar_todos(self):
        speciality1 = new_specialty()
        speciality2 = new_specialty()
        specialties = SpecialtyService.find_all()
        self.assertIsNotNone(specialties)
        self.assertEqual(len(specialties), 2)

    def test_actualizar(self):
        specialty = new_specialty()
        specialty.name = "mathematics updated"
        speciality_actualizada = SpecialtyService.update(specialty.id, specialty)
        self.assertEqual(speciality_actualizada.name, "mathematics updated")

    def test_borrar(self):
        specialty = new_specialty()
        borrado = SpecialtyService.delete_by_id(specialty.id)
        self.assertTrue(borrado)
        resultado = SpecialtyService.find_by_id(specialty.id)
        self.assertIsNone(resultado)