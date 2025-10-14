from django.test import TestCase
from app.models.university import University
from app.services.university_service import UniversityService
from tests.instancias import new_university


class UniversityTestCase(TestCase):
    def test_crear(self):
        university = new_university()
        self.assertIsNotNone(university)
        self.assertIsNotNone(university.id)
        self.assertGreaterEqual(university.id, 1)
        self.assertEqual(university.name, "University Nacional")

    def test_find_by_id(self):
        university = new_university()
        r = UniversityService.find_by_id(university.id)
        self.assertIsNotNone(r)
        self.assertEqual(r.name, "University Nacional")
        self.assertEqual(r.acronym, university.acronym)  # Comparar con la acronym generada
    
    def test_buscar_todos(self):
        universidad1 = new_university()
        universidad2 = new_university()
        universidades = UniversityService.find_all()
        self.assertIsNotNone(universidades)
        self.assertEqual(len(universidades), 2)

    def test_actualizar(self):
        university = new_university()
        university.name = "University Actualizada"
        universidad_actualizada = UniversityService.update(university.id, university)
        self.assertEqual(universidad_actualizada.name, "University Actualizada")

    def test_borrar(self):
        university = new_university()
        borrado = UniversityService.delete_by_id(university.id)
        self.assertTrue(borrado)
        resultado = UniversityService.find_by_id(university.id)
        self.assertIsNone(resultado)
