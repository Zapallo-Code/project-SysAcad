from django.test import TestCase
from app.models import Specialty, SpecialtyType
from app.services import SpecialtyService, SpecialtyTypeService
from tests.instancias import new_specialty, new_specialty_type

class SpecialtyTestCase(TestCase):

    def test_crear(self):
        specialty = new_specialty()
        self.assertIsNotNone(specialty)
        self.assertIsNotNone(specialty.id)
        self.assertGreaterEqual(specialty.id, 1)
        self.assertEqual(specialty.name, "Matematicas")
        self.assertEqual(specialty.specialty_type.name, "Cardiologia")

    def test_find_by_id(self):
        specialty = new_specialty()
        r = SpecialtyService.find_by_id(specialty.id)
        self.assertIsNotNone(r)
        self.assertEqual(r.name, "Matematicas")
        self.assertEqual(r.letter, "A")

    def test_buscar_todos(self):
        especialidad1 = new_specialty()
        especialidad2 = new_specialty()
        specialties = SpecialtyService.find_all()
        self.assertIsNotNone(specialties)
        self.assertEqual(len(specialties), 2)

    def test_actualizar(self):
        specialty = new_specialty()
        specialty.name = "matematica actualizada"
        especialidad_actualizada = SpecialtyService.update(specialty.id, specialty)
        self.assertEqual(especialidad_actualizada.name, "matematica actualizada")

    def test_borrar(self):
        specialty = new_specialty()
        borrado = SpecialtyService.delete_by_id(specialty.id)
        self.assertTrue(borrado)
        resultado = SpecialtyService.find_by_id(specialty.id)
        self.assertIsNone(resultado)