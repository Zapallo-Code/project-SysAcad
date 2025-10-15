from django.test import TestCase
from app.models.department import Department
from app.services import DepartmentService
from tests.fixtures import new_department

class DepartmentTestCase(TestCase):
    
    def test_crear(self):
        departament = new_department()
        self.assertIsNotNone(departament)
        self.assertIsNotNone(departament.id)
        self.assertGreaterEqual(departament.id, 1)
        self.assertEqual(departament.name, "Mathematics")

    def test_find_by_id(self):
        departament = new_department()
        r = DepartmentService.find_by_id(departament.id)
        self.assertIsNotNone(r)
        self.assertEqual(r.name, "Mathematics")
        

    def test_buscar_todos(self):
        departament1 = new_department()
        departament2 = new_department("Physics")
        departments = DepartmentService.find_all()
        self.assertIsNotNone(departments)
        self.assertEqual(len(departments), 2)

    def test_actualizar(self):
        departament = new_department()
        departament.name = "Mathematics updated"
        departament_actualizado = DepartmentService.update(departament.id, departament)
        self.assertEqual(departament_actualizado.name, "Mathematics updated")
    
    def test_borrar(self):
        departament = new_department()
        borrado = DepartmentService.delete_by_id(departament.id)
        self.assertTrue(borrado)
        resultado = DepartmentService.find_by_id(departament.id)
        self.assertIsNone(resultado)