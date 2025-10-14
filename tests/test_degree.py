from django.test import TestCase
from app.models import Degree
from app.services import DegreeService
from tests.fixtures import new_degree


class DegreeTestCase(TestCase):

    def test_crear(self):
        grado = new_degree()
        self.assertIsNotNone(grado)
        self.assertIsNotNone(grado.id)
        self.assertGreaterEqual(grado.id, 1)
        self.assertEqual(grado.name, "First")

    def test_find_by_id(self):
        grado = new_degree()
        r = DegreeService.find_by_id(grado.id)
        self.assertIsNotNone(r)
        self.assertEqual(r.name, "First")
        self.assertEqual(r.description, "Description of the first degree")

    
    def test_buscar_todos(self):
        grado1 = new_degree()
        grado2 = new_degree()
        degrees = DegreeService.find_all()
        self.assertIsNotNone(degrees)
        self.assertGreaterEqual(len(degrees), 2)

    def test_actualizar(self):
        grado = new_degree()
        grado.name = "Second"
        grado.description = "Description of the second degree"

    def test_borrar(self):
        university = new_degree()
        borrado = DegreeService.delete_by_id(university.id)
        self.assertTrue(borrado)
        resultado = DegreeService.find_by_id(university.id)
        self.assertIsNone(resultado)