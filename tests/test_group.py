from django.test import TestCase
from app.models.group import Group
from app.services import GroupService
from tests.fixtures import new_group

class GroupTestCase(TestCase):
        
    def test_find_by_id(self):
        grupo = new_group()
        r = GroupService.find_by_id(grupo.id)
        self.assertIsNotNone(r)
        self.assertEqual(r.name, "Group A")
        
    def test_buscar_todos(self):
        grupo1 = new_group()
        grupo2 = new_group()
        groups = GroupService.find_all()
        self.assertIsNotNone(groups)
        self.assertEqual(len(groups), 2)
        
    def test_actualizar(self):
        grupo = new_group()
        grupo.name = "Group B"
        grupo_actualizado = GroupService.update(grupo.id, grupo)
        self.assertEqual(grupo_actualizado.name, "Group B")

    def test_borrar(self):
        grupo = new_group()
        borrado = GroupService.delete_by_id(grupo.id)
        self.assertTrue(borrado)
        resultado = GroupService.find_by_id(grupo.id)
        self.assertIsNone(resultado)
