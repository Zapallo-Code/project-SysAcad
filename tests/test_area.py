from django.test import TestCase
from app.models.area import Area
from app.services.area import AreaService
from tests.fixtures import new_area


class AreaTestCase(TestCase):
    def test_crear(self):
        area = new_area()
        self.assertIsNotNone(area)
        self.assertIsNotNone(area.id)
        self.assertGreaterEqual(area.id, 1)
        self.assertEqual(area.name, "Mathematics")

    def test_find_by_id(self):
        area = new_area()
        r = AreaService.find_by_id(area.id)
        self.assertIsNotNone(r)
        self.assertEqual(r.name, "Mathematics")

    def test_buscar_todos(self):
        area1 = new_area("Mathematics")
        area2 = new_area("name2")
        areas = AreaService.find_all()
        self.assertIsNotNone(areas)
        self.assertEqual(len(areas), 2)

    def test_actualizar(self):
        area = new_area()
        area.name = "updated name"
        area_actualizado = AreaService.update(area.id, area)
        self.assertEqual(area_actualizado.name, "updated name")

    def test_borrar(self):
        area = new_area()
        borrado = AreaService.delete_by_id(area.id)
        self.assertTrue(borrado)
        resultado = AreaService.find_by_id(area.id)
        self.assertIsNone(resultado)
