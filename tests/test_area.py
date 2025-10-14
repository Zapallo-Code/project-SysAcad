from django.test import TestCase
from app.models.area import Area
from app.services.area_service import AreaService
from tests.instancias import nuevaarea


class AreaTestCase(TestCase):
    def test_crear(self):
        area = nuevaarea()
        self.assertIsNotNone(area)
        self.assertIsNotNone(area.id)
        self.assertGreaterEqual(area.id, 1)
        self.assertEqual(area.nombre, "Matematica")

    def test_find_by_id(self):
        area = nuevaarea()
        r = AreaService.find_by_id(area.id)
        self.assertIsNotNone(r)
        self.assertEqual(r.nombre, "Matematica")

    def test_buscar_todos(self):
        area1 = nuevaarea("Matematica")
        area2 = nuevaarea("nombre2")
        areas = AreaService.buscar_todos()
        self.assertIsNotNone(areas)
        self.assertEqual(len(areas), 2)

    def test_actualizar(self):
        area = nuevaarea()
        area.nombre = "nombre actualizado"
        area_actualizado = AreaService.actualizar(area.id, area)
        self.assertEqual(area_actualizado.nombre, "nombre actualizado")

    def test_borrar(self):
        area = nuevaarea()
        borrado = AreaService.borrar_por_id(area.id)
        self.assertTrue(borrado)
        resultado = AreaService.find_by_id(area.id)
        self.assertIsNone(resultado)
