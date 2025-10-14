from django.test import TestCase
from app.models import SpecialtyType
from app.services import SpecialtyTypeService
from tests.instancias import new_specialty_type


class SpecialtyTypeTestCase(TestCase):

    def test_crear(self):
        specialty_type = new_specialty_type()
        self.assertIsNotNone(specialty_type)
        self.assertIsNotNone(specialty_type.id)
        self.assertGreaterEqual(specialty_type.id, 1)    
        self.assertEqual(specialty_type.name, "Cardiologia")
        self.assertEqual(specialty_type.level, "Avanzado")

    def test_find_by_id(self):
        specialty_type = new_specialty_type()
        r = SpecialtyTypeService.find_by_id(specialty_type.id)
        self.assertIsNotNone(r)
        self.assertEqual(r.name, specialty_type.name)
    
    def test_buscar_todos(self):
        tipoespecialidad1 = new_specialty_type()
        tipoespecialidad2 = new_specialty_type("pediatria", "Basico")
        specialty_type = SpecialtyTypeService.find_all()
        self.assertIsNotNone(specialty_type)
        self.assertGreaterEqual(len(specialty_type), 2)

    def test_actualizar(self):
        specialty_type = new_specialty_type()
        specialty_type.name = "Neurología"
        specialty_type.level = "Intermedio"
        tipoespecialidad_actualizado = SpecialtyTypeService.update(specialty_type.id, specialty_type)
        self.assertEqual(tipoespecialidad_actualizado.name, "Neurología")
        self.assertEqual(tipoespecialidad_actualizado.level, "Intermedio")

    def test_borrar(self):
        specialty_type = new_specialty_type()
        borrado = SpecialtyTypeService.delete_by_id(specialty_type.id)
        self.assertTrue(borrado)
        resultado = SpecialtyTypeService.find_by_id(specialty_type.id)
        self.assertIsNone(resultado)
