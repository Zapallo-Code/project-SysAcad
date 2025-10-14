from django.test import TestCase
from app.models.position_category import PositionCategory
from app.services.position_category import PositionCategoryService
from tests.fixtures import new_position_category


class PositionCategoryTestCase(TestCase):
    def test_crear(self):
        categoria = new_position_category()
        self.assertIsNotNone(categoria)
        self.assertIsNotNone(categoria.id)
        self.assertGreaterEqual(categoria.id, 1)
        self.assertEqual(categoria.name, "Teacher")

    def test_find_by_id(self):
        categoria = new_position_category()
        r = PositionCategoryService.find_by_id(categoria.id)
        self.assertIsNotNone(r)
        self.assertEqual(r.name, "Teacher")
    
    def test_buscar_todos(self):
        categoria1 = new_position_category()
        categoria2 = new_position_category()
        categorias = PositionCategoryService.find_all()
        self.assertIsNotNone(categorias)
        self.assertEqual(len(categorias), 2)

    def test_actualizar(self):
        categoria = new_position_category()
        categoria.name = "Teacher updated"
        categoria_actualizado = PositionCategoryService.update(categoria.id, categoria)
        self.assertEqual(categoria_actualizado.name, "Teacher updated")

    def test_borrar(self):
        categoria = new_position_category()
        borrado = PositionCategoryService.delete_by_id(categoria.id)
        self.assertTrue(borrado)
        resultado = PositionCategoryService.find_by_id(categoria.id)
        self.assertIsNone(resultado)

    
        