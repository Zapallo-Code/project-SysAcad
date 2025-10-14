from django.test import TestCase
from datetime import date
from app.models.document_type import DocumentType
from app.models.student import Student
from app.services.student import StudentService
from app.services.document_type import DocumentTypeService
from tests.fixtures import new_student, new_document_type


class StudentTestCase(TestCase):
    def test_crear(self):
        student = new_student()
        self.assertIsNotNone(student)
        self.assertIsNotNone(student.first_name)
        self.assertGreaterEqual(student.id, 1)
        self.assertEqual(student.last_name, "Pérez")
        self.assertEqual(student.document_type.passport, "nacnal")

    def test_find_by_id(self):
        student = new_student()
        r = StudentService.find_by_id(student.id)
        self.assertIsNotNone(r)
        self.assertEqual(r.first_name, "Juan")
        self.assertEqual(r.last_name, "Pérez")

    def test_buscar_todos(self):
        alumno1 = new_student()
        tipo_doc2 = new_document_type(
            dni="50291002",
            civic_card="l",
            enrollment_card="aci",
            passport="nacn")
    
        alumno2 = new_student(
            first_name="Pedro",
            last_name="Gómez",
            document_number="12345678",
            document_type=tipo_doc2,
            birth_date=date(1995, 5, 5),
            gender="M",
            student_number=654321,
            enrollment_date=date(2021, 1, 1))
        
        students = StudentService.find_all()
        self.assertIsNotNone(students)
        self.assertEqual(len(students), 2)

    def test_actualizar(self):
        student = new_student()
        student.first_name = "Juan actualizado"
        updated_student = StudentService.update(student.id, student)
        self.assertEqual(updated_student.first_name, "Juan actualizado")
    
    def test_borrar(self):
        student = new_student()
        borrado = StudentService.delete_by_id(student.id)
        self.assertTrue(borrado)
        resultado = StudentService.find_by_id(student.id)
        self.assertIsNone(resultado)


        