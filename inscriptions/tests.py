from django.test import TestCase
from app.models import SubjectInscription, FinalExamInscription, CustomUser, Student, Subject, FinalExam, Career, Faculty
import datetime


class SubjectInscriptionModelTest(TestCase):
    def setUp(self):
        self.faculty = Faculty.objects.create(
            code='F1',
            name='Facultad de Ingeniería',
            dean='Decano Ejemplo',
            established_date='1950-01-01'
        )
        self.career = Career.objects.create(
            name='Ingeniería',
            code='ING',
            faculty=self.faculty,
            director='Director',
            duration_years=5
        )
        self.subject = Subject.objects.create(
            name='Matemática',
            code='MAT101',
            career=self.career,
            year=1,
            category=Subject.Category.OBLIGATORY,
            period=Subject.Period.FIRST,
            semanal_hours=6
        )
        self.user = CustomUser.objects.create_user(
            username='student1',
            password='testpass',
            role=CustomUser.Role.STUDENT,
            dni='12345678'
        )
        self.student = Student.objects.create(
            student_id='S1',
            user=self.user,
            career=self.career,
            enrollment_date='2022-01-01'
        )

    def test_create_subject_inscription(self):
        inscription = SubjectInscription.objects.create(
            student=self.student,
            subject=self.subject
        )
        self.assertEqual(inscription.student.user.username, 'student1')
        self.assertEqual(inscription.subject.name, 'Matemática')
        self.assertIsNotNone(inscription.inscription_date)
        self.assertIn('student1', str(inscription))


class FinalExamInscriptionModelTest(TestCase):
    def setUp(self):
        self.faculty = Faculty.objects.create(
            code='F1',
            name='Facultad de Ingeniería',
            dean='Decano Ejemplo',
            established_date='1950-01-01'
        )
        self.career = Career.objects.create(
            name='Ingeniería',
            code='ING',
            faculty=self.faculty,
            director='Director',
            duration_years=5
        )
        self.subject = Subject.objects.create(
            name='Matemática',
            code='MAT101',
            career=self.career,
            year=1,
            category=Subject.Category.OBLIGATORY,
            period=Subject.Period.FIRST,
            semanal_hours=6
        )
        self.final_exam = FinalExam.objects.create(
            subject=self.subject,
            date=datetime.date(2024, 7, 1),
            location='Aula 1',
            duration='02:00:00',
            call_number=1
        )
        self.user = CustomUser.objects.create_user(
            username='student1',
            password='testpass',
            role=CustomUser.Role.STUDENT,
            dni='12345678'
        )
        self.student = Student.objects.create(
            student_id='S1',
            user=self.user,
            career=self.career,
            enrollment_date='2022-01-01'
        )

    def test_create_final_exam_inscription(self):
        inscription = FinalExamInscription.objects.create(
            student=self.student,
            final_exam=self.final_exam
        )
        self.assertEqual(inscription.student.user.username, 'student1')
        self.assertEqual(inscription.final_exam.subject.name, 'Matemática')
        self.assertIsNotNone(inscription.inscription_date)
        self.assertIn('student1', str(inscription))
