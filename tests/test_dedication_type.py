from django.test import TestCase
from app.models.dedication_type import DedicationType
from app.services import DedicationTypeService
from tests.fixtures import new_dedication_type

class DedicationTypeTestCase(TestCase):

    def test_crear(self):
        dedication_type = new_dedication_type()
        self.assertIsNotNone(dedication_type)
        self.assertIsNotNone(dedication_type.id)
        self.assertGreaterEqual(dedication_type.id, 1)
        self.assertEqual(dedication_type.name, "Full Dedication")
        self.assertEqual(dedication_type.observation, "Test observation")

    def test_find_by_id(self):
        dedication_type = new_dedication_type()
        r = DedicationTypeService.find_by_id(dedication_type.id)
        self.assertIsNotNone(r)
        self.assertEqual(r.name, "Full Dedication")
        self.assertEqual(r.observation, "Test observation")
    
    def test_buscar_todos(self):
        dedication_type1 = new_dedication_type()
        dedication_type2 = new_dedication_type("Dedicacion Completa 2", "Observacion de prueba 2")
        dedicaciones = DedicationTypeService.find_all()
        self.assertIsNotNone(dedicaciones)
        self.assertEqual(len(dedicaciones), 2)

    def test_actualizar(self):
        dedication_type = new_dedication_type()
        dedication_type.name = "Dedicacion actualizada"
        dedication_type_actualizado = DedicationTypeService.update(dedication_type.id, dedication_type)
        self.assertEqual(dedication_type_actualizado.name, "Dedicacion actualizada")

    def test_borrar(self):
        dedication_type = new_dedication_type()
        borrado = DedicationTypeService.delete_by_id(dedication_type.id)
        self.assertTrue(borrado)
        resultado = DedicationTypeService.find_by_id(dedication_type.id)
        self.assertIsNone(resultado)