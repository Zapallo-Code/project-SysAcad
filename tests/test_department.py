from django.test import TestCase
from app.models.department import Department
from app.services import DepartmentService
from tests.fixtures import new_department

class DepartmentTestCase(TestCase):
    
    def test_crear(self):
        departamento = new_department()
        self.assertIsNotNone(departamento)
        self.assertIsNotNone(departamento.id)
        self.assertGreaterEqual(departamento.id, 1)
        self.assertEqual(departamento.name, "Mathematics")

    def test_find_by_id(self):
        departamento = new_department()
        r = DepartmentService.find_by_id(departamento.id)
        self.assertIsNotNone(r)
        self.assertEqual(r.name, "Mathematics")
        

    def test_buscar_todos(self):
        departamento1 = new_department()
        departamento2 = new_department("Physics")
        departments = DepartmentService.find_all()
        self.assertIsNotNone(departments)
        self.assertEqual(len(departments), 2)

    def test_actualizar(self):
        departamento = new_department()
        departamento.name = "Mathematics updated"
        departamento_actualizado = DepartmentService.update(departamento.id, departamento)
        self.assertEqual(departamento_actualizado.name, "Mathematics updated")
    
    def test_borrar(self):
        departamento = new_department()
        borrado = DepartmentService.delete_by_id(departamento.id)
        self.assertTrue(borrado)
        resultado = DepartmentService.find_by_id(departamento.id)
        self.assertIsNone(resultado)