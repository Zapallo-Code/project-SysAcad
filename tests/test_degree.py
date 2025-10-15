from django.test import TestCase
from app.models import Degree
from app.services import DegreeService
from tests.fixtures import new_degree


class DegreeTestCase(TestCase):

    def test_crear(self):
        degree = new_degree()
        self.assertIsNotNone(degree)
        self.assertIsNotNone(degree.id)
        self.assertGreaterEqual(degree.id, 1)
        self.assertEqual(degree.name, "First")

    def test_find_by_id(self):
        degree = new_degree()
        r = DegreeService.find_by_id(degree.id)
        self.assertIsNotNone(r)
        self.assertEqual(r.name, "First")
        self.assertEqual(r.description, "Description of the first degree")

    
    def test_buscar_todos(self):
        degree1 = new_degree()
        degree2 = new_degree()
        degrees = DegreeService.find_all()
        self.assertIsNotNone(degrees)
        self.assertGreaterEqual(len(degrees), 2)

    def test_actualizar(self):
        degree = new_degree()
        degree.name = "Second"
        degree.description = "Description of the second degree"

    def test_borrar(self):
        university = new_degree()
        borrado = DegreeService.delete_by_id(university.id)
        self.assertTrue(borrado)
        resultado = DegreeService.find_by_id(university.id)
        self.assertIsNone(resultado)