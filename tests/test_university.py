from django.test import TestCase
from app.models.university import University
from app.services.university import UniversityService
from tests.fixtures import new_university


class UniversityTestCase(TestCase):
    def test_crear(self):
        university = new_university()
        self.assertIsNotNone(university)
        self.assertIsNotNone(university.id)
        self.assertGreaterEqual(university.id, 1)
        self.assertEqual(university.name, "National University")

    def test_find_by_id(self):
        university = new_university()
        r = UniversityService.find_by_id(university.id)
        self.assertIsNotNone(r)
        self.assertEqual(r.name, "National University")
        self.assertEqual(r.acronym, university.acronym)  # Comparar con la acronym generada
    
    def test_buscar_todos(self):
        university1 = new_university()
        university2 = new_university()
        universityes = UniversityService.find_all()
        self.assertIsNotNone(universityes)
        self.assertEqual(len(universityes), 2)

    def test_actualizar(self):
        university = new_university()
        university.name = "Updated University"
        university_actualizada = UniversityService.update(university.id, university)
        self.assertEqual(university_actualizada.name, "Updated University")

    def test_borrar(self):
        university = new_university()
        borrado = UniversityService.delete_by_id(university.id)
        self.assertTrue(borrado)
        resultado = UniversityService.find_by_id(university.id)
        self.assertIsNone(resultado)
