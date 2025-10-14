from django.test import TestCase
from app.models import Subject, Authority
from app.services import SubjectService, AuthorityService
from tests.instancias import new_subject, new_authority

class SubjectTestCase(TestCase):

    def test_crear(self):
        authority = new_authority(name="Authority 1")
        subject = new_subject(authorities=[authority])
        self.assertIsNotNone(subject.id)
        self.assertEqual(subject.name, "Matematica")
        self.assertIn(authority, subject.authorities.all())

    def test_find_by_id(self):
        subject = new_subject()
        encontrado = SubjectService.find_by_id(subject.id)
        self.assertIsNotNone(encontrado)
        self.assertEqual(encontrado.name, subject.name)

    def test_buscar_todos(self):
        materia1 = new_subject(name="Matematica 1", code="MAT1")
        materia2 = new_subject(name="Matematica 2", code="MAT2")
        subjects = SubjectService.find_all()
        self.assertIsNotNone(subjects)
        self.assertGreaterEqual(len(subjects), 2)
        nombres = [m.name for m in subjects]
        self.assertIn("Matematica 1", nombres)
        self.assertIn("Matematica 2", nombres)

    def test_actualizar(self):
        subject = new_subject()
        subject.name = "Nombre Actualizado"
        actualizado = SubjectService.update(subject.id, subject)
        self.assertEqual(actualizado.name, "Nombre Actualizado")

    def test_borrar(self):
        subject = new_subject()
        borrado = SubjectService.delete_by_id(subject.id)
        self.assertTrue(borrado)
        resultado = SubjectService.find_by_id(subject.id)
        self.assertIsNone(resultado)

    def test_asociar_y_desasociar_autoridad(self):
        subject = new_subject()
        authority = new_authority()
        
        # Asociar authority
        SubjectService.asociar_autoridad(subject.id, authority.id)
        materia_actualizada = SubjectService.find_by_id(subject.id)
        self.assertIn(authority, materia_actualizada.authorities.all())
        
        # Desasociar authority
        SubjectService.desasociar_autoridad(subject.id, authority.id)
        materia_actualizada = SubjectService.find_by_id(subject.id)
        self.assertNotIn(authority, materia_actualizada.authorities.all())
