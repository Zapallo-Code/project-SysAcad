from django.test import TestCase
from app.models import Degree
from app.services import DegreeService
from tests.instancias import new_degree


class DegreeTestCase(TestCase):

    def test_crear(self):
        grado = new_degree()
        self.assertIsNotNone(grado)
        self.assertIsNotNone(grado.id)
        self.assertGreaterEqual(grado.id, 1)
        self.assertEqual(grado.name, "Primero")

    def test_find_by_id(self):
        grado = new_degree()
        r = DegreeService.find_by_id(grado.id)
        self.assertIsNotNone(r)
        self.assertEqual(r.name, "Primero")
        self.assertEqual(r.description, "Descripcion del primer grado")

    
    def test_buscar_todos(self):
        grado1 = new_degree()
        grado2 = new_degree()
        degrees = DegreeService.find_all()
        self.assertIsNotNone(degrees)
        self.assertGreaterEqual(len(degrees), 2)

    def test_actualizar(self):
        grado = new_degree()
        grado.name = "Segundo"
        grado.description = "Descripción del segundo grado"

    def test_borrar(self):
        university = new_degree()
        borrado = DegreeService.delete_by_id(university.id)
        self.assertTrue(borrado)
        resultado = DegreeService.find_by_id(university.id)
        self.assertIsNone(resultado)