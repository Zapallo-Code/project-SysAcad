from django.test import TestCase
from app.models.authority import Authority
from app.models.subject import Subject
from app.services.authority import AuthorityService
from tests.fixtures import new_authority, new_subject, new_faculty


class AuthorityTestCase(TestCase):
    def test_crear(self):
        faculty = new_faculty()
        subject = new_subject()
        authority = new_authority(subjects=[subject], faculties=[faculty])
        self.assertIsNotNone(authority.id)
        self.assertEqual(authority.name, "Pelo")
        self.assertIn(subject, authority.subjects.all())
        self.assertIn(faculty, authority.faculties.all())

    def test_find_by_id(self):
        authority = new_authority()
        encontrado = AuthorityService.find_by_id(authority.id)
        self.assertIsNotNone(encontrado)
        self.assertEqual(encontrado.name, authority.name)

    def test_buscar_todos(self):
        authority1 = new_authority(name="Pelo1")
        authority2 = new_authority(name="Pelo2")
        authorities = AuthorityService.find_all()
        self.assertIsNotNone(authorities)
        self.assertGreaterEqual(len(authorities), 2)
        nombres = [a.name for a in authorities]
        self.assertIn("Pelo1", nombres)
        self.assertIn("Pelo2", nombres)

    def test_actualizar(self):
        authority = new_authority()
        authority.name = "Nombre Actualizado"
        actualizado = AuthorityService.update(authority.id, authority)
        self.assertEqual(actualizado.name, "Nombre Actualizado")

    def test_borrar(self):
        authority = new_authority()
        borrado = AuthorityService.delete_by_id(authority.id)
        self.assertTrue(borrado)
        resultado = AuthorityService.find_by_id(authority.id)
        self.assertIsNone(resultado)

    def test_relacion_subjects(self):
        authority = new_authority()
        subject1 = new_subject(name="Matematica")
        subject2 = new_subject(name="Fisica")

        authority.subjects.add(subject1)
        authority.subjects.add(subject2)
        authority.save()

        self.assertIn(subject1, authority.subjects.all())
        self.assertIn(subject2, authority.subjects.all())
        self.assertIn(authority, subject1.authorities.all())
        self.assertIn(authority, subject2.authorities.all())

        authority.subjects.remove(subject1)
        authority.save()
        self.assertNotIn(subject1, authority.subjects.all())
        self.assertNotIn(authority, subject1.authorities.all())

    def test_asociar_y_desasociar_subject(self):
        authority = new_authority()
        subject = new_subject()

        AuthorityService.associate_subject(authority.id, subject.id)
        authority_actualizada = AuthorityService.find_by_id(authority.id)
        self.assertIn(subject, authority_actualizada.subjects.all())

        AuthorityService.disassociate_subject(authority.id, subject.id)
        authority_actualizada = AuthorityService.find_by_id(authority.id)
        self.assertNotIn(subject, authority_actualizada.subjects.all())

    def test_asociar_y_desasociar_faculty(self):
        faculty = new_faculty()
        authority = new_authority()

        AuthorityService.associate_faculty(authority.id, faculty.id)
        authority_actualizada = AuthorityService.find_by_id(authority.id)
        self.assertIn(faculty, authority_actualizada.faculties.all())

        AuthorityService.disassociate_faculty(authority.id, faculty.id)
        authority_actualizada = AuthorityService.find_by_id(authority.id)
        self.assertNotIn(faculty, authority_actualizada.faculties.all())
