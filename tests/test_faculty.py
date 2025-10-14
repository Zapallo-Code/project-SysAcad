from django.test import TestCase
from app.models.faculty import Faculty
from app.services.faculty_service import FacultyService
from tests.fixtures import new_faculty, new_authority

class FacultyTestCase(TestCase):

    def test_crear(self):
        authority = new_authority()
        faculty = new_faculty(authorities=[authority])
        self.assertIsNotNone(faculty)
        self.assertIsNotNone(faculty.id)
        self.assertIsNotNone(faculty.university)
        self.assertEqual(faculty.university.name, "National University")
        self.assertGreaterEqual(faculty.id, 1)
        self.assertEqual(faculty.name, "Faculty of Sciences")
        self.assertIn(authority, faculty.authorities.all())

    def test_find_by_id(self):
        authority = new_authority()
        faculty = new_faculty(authorities=[authority])
        r = FacultyService.find_by_id(faculty.id)
        self.assertIsNotNone(r)
        self.assertEqual(r.name, "Faculty of Sciences")
        self.assertEqual(list(r.authorities.all())[0].name, authority.name)

    def test_buscar_todos(self):
        facultad1 = new_faculty()
        facultad2 = new_faculty(name="Faculty of Mathematics")
        faculties = FacultyService.find_all()
        self.assertIsNotNone(faculties)
        self.assertEqual(len(faculties), 2)
        nombres = [f.name for f in faculties]
        self.assertIn("Faculty of Sciences", nombres)
        self.assertIn("Faculty of Mathematics", nombres)


    def test_actualizar(self):
        faculty = new_faculty()
        faculty.name = "Faculty of Sciences Updated"
        facultad_actualizada = FacultyService.update(faculty.id, faculty)
        self.assertEqual(facultad_actualizada.name, "Faculty of Sciences Updated")

    def test_borrar(self):
        faculty = new_faculty()
        borrado = FacultyService.delete_by_id(faculty.id)
        self.assertTrue(borrado)
        resultado = FacultyService.find_by_id(faculty.id)
        self.assertIsNone(resultado)
    
    def test_asociar_y_desasociar_autoridad(self):
        faculty = new_faculty()
        authority = new_authority()
        
        # Asociar authority
        FacultyService.associate_authority(faculty.id, authority.id)
        facultad_actualizada = FacultyService.find_by_id(faculty.id)
        self.assertIn(authority, facultad_actualizada.authorities.all())
        
        # Desasociar authority
        FacultyService.disassociate_authority(faculty.id, authority.id)
        facultad_actualizada = FacultyService.find_by_id(faculty.id)
        self.assertNotIn(authority, facultad_actualizada.authorities.all())
