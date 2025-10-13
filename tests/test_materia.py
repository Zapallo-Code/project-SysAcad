import unittest
from app import create_app, db
from app.models import Materia, Autoridad
from app.services import MateriaService, AutoridadService
from test.instancias import nuevamateria, nuevaautoridad

class MateriaTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_crear(self):
        autoridad = nuevaautoridad(nombre="Autoridad 1")
        materia = nuevamateria(autoridades=[autoridad])
        self.assertIsNotNone(materia.id)
        self.assertEqual(materia.nombre, "Matematica")
        self.assertIn(autoridad, materia.autoridades)

    def test_buscar_por_id(self):
        materia = nuevamateria()
        encontrado = MateriaService.buscar_por_id(materia.id)
        self.assertIsNotNone(encontrado)
        self.assertEqual(encontrado.nombre, materia.nombre)

    def test_buscar_todos(self):
        materia1 = nuevamateria(nombre="Matematica 1")
        materia2 = nuevamateria(nombre="Matematica 2")
        materias = MateriaService.buscar_todos()
        self.assertIsNotNone(materias)
        self.assertGreaterEqual(len(materias), 2)
        nombres = [m.nombre for m in materias]
        self.assertIn("Matematica 1", nombres)
        self.assertIn("Matematica 2", nombres)

    def test_actualizar(self):
        materia = nuevamateria()
        materia.nombre = "Nombre Actualizado"
        actualizado = MateriaService.actualizar(materia.id, materia)
        self.assertEqual(actualizado.nombre, "Nombre Actualizado")

    def test_borrar(self):
        materia = nuevamateria()
        borrado = MateriaService.borrar_por_id(materia.id)
        self.assertTrue(borrado)
        resultado = MateriaService.buscar_por_id(materia.id)
        self.assertIsNone(resultado)

    def test_asociar_y_desasociar_autoridad(self):
        materia = nuevamateria()
        autoridad = nuevaautoridad()
        
        # Asociar autoridad
        MateriaService.asociar_autoridad(materia.id, autoridad.id)
        materia_actualizada = MateriaService.buscar_por_id(materia.id)
        self.assertIn(autoridad, materia_actualizada.autoridades)
        
        # Desasociar autoridad
        MateriaService.desasociar_autoridad(materia.id, autoridad.id)
        materia_actualizada = MateriaService.buscar_por_id(materia.id)
        self.assertNotIn(autoridad, materia_actualizada.autoridades)
