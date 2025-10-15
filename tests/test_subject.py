from django.test import TestCase
from app.models import Subject, Authority
from app.services import SubjectService, AuthorityService
from tests.fixtures import new_subject, new_authority

class SubjectTestCase(TestCase):

    def test_crear(self):
        authority = new_authority(name="Authority 1")
        subject = new_subject(authorities=[authority])
        self.assertIsNotNone(subject.id)
        self.assertEqual(subject.name, "Mathematics")
        self.assertIn(authority, subject.authorities.all())

    def test_find_by_id(self):
        subject = new_subject()
        encontrado = SubjectService.find_by_id(subject.id)
        self.assertIsNotNone(encontrado)
        self.assertEqual(encontrado.name, subject.name)

    def test_buscar_todos(self):
        subject1 = new_subject(name="Mathematics 1", code="MAT1")
        subject2 = new_subject(name="Mathematics 2", code="MAT2")
        subjects = SubjectService.find_all()
        self.assertIsNotNone(subjects)
        self.assertGreaterEqual(len(subjects), 2)
        nombres = [m.name for m in subjects]
        self.assertIn("Mathematics 1", nombres)
        self.assertIn("Mathematics 2", nombres)

    def test_actualizar(self):
        subject = new_subject()
        subject.name = "Updated Name"
        actualizado = SubjectService.update(subject.id, subject)
        self.assertEqual(actualizado.name, "Updated Name")

    def test_borrar(self):
        subject = new_subject()
        borrado = SubjectService.delete_by_id(subject.id)
        self.assertTrue(borrado)
        resultado = SubjectService.find_by_id(subject.id)
        self.assertIsNone(resultado)

    def test_asociar_y_desasociar_authority(self):
        subject = new_subject()
        authority = new_authority()
        
        # Asociar authority
        SubjectService.associate_authority(subject.id, authority.id)
        subject_actualizada = SubjectService.find_by_id(subject.id)
        self.assertIn(authority, subject_actualizada.authorities.all())
        
        # Desasociar authority
        SubjectService.disassociate_authority(subject.id, authority.id)
        subject_actualizada = SubjectService.find_by_id(subject.id)
        self.assertNotIn(authority, subject_actualizada.authorities.all())
