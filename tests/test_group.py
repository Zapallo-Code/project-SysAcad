from django.test import TestCase
from app.models.group import Group
from app.services import GroupService
from tests.fixtures import new_group

class GroupTestCase(TestCase):
        
    def test_find_by_id(self):
        group = new_group()
        r = GroupService.find_by_id(group.id)
        self.assertIsNotNone(r)
        self.assertEqual(r.name, "Group A")
        
    def test_buscar_todos(self):
        group1 = new_group()
        group2 = new_group()
        groups = GroupService.find_all()
        self.assertIsNotNone(groups)
        self.assertEqual(len(groups), 2)
        
    def test_actualizar(self):
        group = new_group()
        group.name = "Group B"
        group_actualizado = GroupService.update(group.id, group)
        self.assertEqual(group_actualizado.name, "Group B")

    def test_borrar(self):
        group = new_group()
        borrado = GroupService.delete_by_id(group.id)
        self.assertTrue(borrado)
        resultado = GroupService.find_by_id(group.id)
        self.assertIsNone(resultado)
