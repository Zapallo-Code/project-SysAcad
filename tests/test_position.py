from django.test import TestCase
from app.models.position import Position
from app.models.position_category import PositionCategory
from app.models.dedication_type import DedicationType
from app.services.position_service import PositionService
from tests.instancias import new_position


class PositionTestCase(TestCase):
    def test_crear(self):
        position = new_position()
        self.assertIsNotNone(position)
        self.assertIsNotNone(position.name)
        self.assertGreaterEqual(position.name, "Profesor")
        self.assertEqual(position.position_category.name, "Docente")
        self.assertEqual(position.dedication_type.name, "Dedicacion Completa")

    def test_find_by_id(self):
        position = new_position()
        r = PositionService.find_by_id(position.id)
        self.assertIsNotNone(r)
        self.assertEqual(r.name, "Profesor")
        self.assertEqual(r.dedication_type.name, "Dedicacion Completa")

    def test_buscar_todos(self):
        cargo1 = new_position()
        cargo2 = new_position()
        positions = PositionService.find_all()
        self.assertIsNotNone(positions)
        self.assertEqual(len(positions), 2)

    def test_actualizar(self):
        position = new_position()
        position.name = "profe actualizado"
        cargo_actualizado = PositionService.update(position.id, position)
        self.assertEqual(cargo_actualizado.name, "profe actualizado")

    def test_borrar(self):
        position = new_position()
        borrado = PositionService.delete_by_id(position.id)
        self.assertTrue(borrado)
        resultado = PositionService.find_by_id(position.id)
        self.assertIsNone(resultado)
    