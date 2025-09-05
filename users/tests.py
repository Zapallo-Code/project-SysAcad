from datetime import date, timedelta
from unittest.mock import patch
from tempfile import TemporaryDirectory

from django.test import TestCase, override_settings
from django.urls import reverse

from app.models import Career, Faculty, FinalExam, Grade, Subject, FinalExamInscription, SubjectInscription, Administrator, CustomUser, Professor, Student


class CustomUserModelTest(TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass',
            role=CustomUser.Role.STUDENT,
            dni='12345678'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.role, CustomUser.Role.STUDENT)
        self.assertEqual(user.dni, '12345678')


class StudentModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='student1',
            password='testpass',
            role=CustomUser.Role.STUDENT,
            dni='87654321'
        )
        self.faculty = Faculty.objects.create(
            code='F1',
            name='Facultad de Ingeniería',
            dean='Decano Ejemplo',
            established_date='1950-01-01'
        )
        self.career = Career.objects.create(
            name='Ingeniería',
            code='ING',
            faculty_id='F1',
            director='Director',
            duration_years=5
        )

    def test_create_student(self):
        student = Student.objects.create(
            student_id='S1',
            user=self.user,
            career=self.career,
            enrollment_date='2022-01-01'
        )
        self.assertEqual(student.user.username, 'student1')
        self.assertEqual(student.career.name, 'Ingeniería')


class ProfessorModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='prof1',
            password='testpass',
            role=CustomUser.Role.PROFESSOR,
            dni='11223344'
        )

    def test_create_professor(self):
        professor = Professor.objects.create(
            professor_id='P1',
            user=self.user,
            degree='PhD',
            hire_date='2020-01-01',
            category=Professor.Category.TITULAR
        )
        self.assertEqual(professor.user.username, 'prof1')
        self.assertEqual(professor.category, Professor.Category.TITULAR)


class AdministratorModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='admin1',
            password='testpass',
            role=CustomUser.Role.ADMIN,
            dni='99887766'
        )

    def test_create_administrator(self):
        admin = Administrator.objects.create(
            administrator_id='A1',
            user=self.user,
            position='Manager',
            hire_date='2021-01-01'
        )
        self.assertEqual(admin.user.username, 'admin1')
        self.assertEqual(admin.position, 'Manager')


def make_admin(username="admin", dni="90000000"):
    user = CustomUser.objects.create_user(
        username=username,
        password="pass1234",
        role=CustomUser.Role.ADMIN,
        dni=dni,
    )
    Administrator.objects.create(
        administrator_id=f"A-{dni}", user=user, position="Mgr", hire_date=date(2020, 1, 1)
    )
    return user


def make_faculty(code="F1"):
    return Faculty.objects.create(
        code=code,
        name="Facultad de Ingeniería",
        address="Calle 123",
        phone="123456789",
        email="facu@uni.edu",
        website="https://facu.uni.edu",
        dean="Decano",
        established_date=date(1950, 1, 1),
        description="desc",
    )


def make_career(code="ING", faculty=None):
    faculty = faculty or make_faculty()
    return Career.objects.create(
        name="Ingeniería", code=code, faculty=faculty, director="Director", duration_years=5
    )


def make_subject(code="MAT101", career=None):
    career = career or make_career()
    return Subject.objects.create(
        name="Matemática",
        code=code,
        career=career,
        year=1,
        category=Subject.Category.OBLIGATORY,
        period=Subject.Period.FIRST,
        semanal_hours=6,
    )


def make_student(username="stud", dni="10000001", career=None):
    user = CustomUser.objects.create_user(
        username=username,
        password="pass1234",
        role=CustomUser.Role.STUDENT,
        dni=dni,
    )
    student = Student.objects.create(
        student_id=f"S-{dni}", user=user, career=career or make_career(), enrollment_date=date(2020, 1, 1)
    )
    return user, student


def make_professor(username="prof", dni="10000002"):
    user = CustomUser.objects.create_user(
        username=username,
        password="pass1234",
        role=CustomUser.Role.PROFESSOR,
        dni=dni,
    )
    prof = Professor.objects.create(
        professor_id=f"P-{dni}",
        user=user,
        degree="Ing.",
        hire_date=date(2019, 1, 1),
        category=Professor.Category.TITULAR,
    )
    return user, prof


class AdminViewsTests(TestCase):
    def setUp(self):
        self.admin = make_admin()

    def test_admin_dashboard_requires_admin(self):
        # Unauthenticated -> redirect to login
        resp = self.client.get(reverse("users:admin-dashboard"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/login", resp["Location"])  # login redirect

        # Authenticated admin -> OK
        self.client.force_login(self.admin)
        resp = self.client.get(reverse("users:admin-dashboard"))
        self.assertEqual(resp.status_code, 200)

    def test_user_list_visible_to_admin(self):
        self.client.force_login(self.admin)
        resp = self.client.get(reverse("users:user-list"))
        self.assertEqual(resp.status_code, 200)

    def test_user_create_admin_role(self):
        self.client.force_login(self.admin)
        payload = {
            "username": "newadmin",
            "first_name": "Ana",
            "last_name": "Admin",
            "email": "ana@example.com",
            "dni": "80000000",
            "role": CustomUser.Role.ADMIN,
            "is_active": True,
            "password1": "Passw0rd!",
            "password2": "Passw0rd!",
            # Admin profile
            "administrator_id": "A-80000000",
            "position": "Ops",
            "hire_date": "2021-01-01",
        }
        resp = self.client.post(reverse("users:user-create"), data=payload)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(CustomUser.objects.filter(username="newadmin").exists())
        created = CustomUser.objects.get(username="newadmin")
        self.assertEqual(created.role, CustomUser.Role.ADMIN)
        self.assertTrue(hasattr(created, "administrator"))

    def test_faculty_crud(self):
        self.client.force_login(self.admin)
        # Create
        create_payload = {
            "name": "Facultad X",
            "code": "FX",
            "address": "Dir 1",
            "phone": "123",
            "email": "fx@u.edu",
            "website": "https://fx.u.edu",
            "dean": "Decano X",
            "established_date": "2000-01-01",
            "description": "desc",
        }
        resp = self.client.post(reverse("users:faculty-create"), data=create_payload)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Faculty.objects.filter(code="FX").exists())

        # Edit
        edit_payload = create_payload | {"name": "Facultad X Edit"}
        resp = self.client.post(reverse("users:faculty-edit", args=["FX"]), data=edit_payload)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Faculty.objects.get(code="FX").name, "Facultad X Edit")

        # Delete
        resp = self.client.post(reverse("users:faculty-delete", args=["FX"]))
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Faculty.objects.filter(code="FX").exists())

    def test_career_crud(self):
        self.client.force_login(self.admin)
        fac = make_faculty("FZ")
        # Create
        create_payload = {
            "name": "Carrera Y",
            "code": "CY",
            "faculty": fac.code,
            "director": "Dir Y",
            "duration_years": 4,
            "description": "desc",
        }
        resp = self.client.post(reverse("users:career-create"), data=create_payload)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Career.objects.filter(code="CY").exists())

        # Edit
        edit_payload = create_payload | {"name": "Carrera Y Edit"}
        resp = self.client.post(reverse("users:career-edit", args=["CY"]), data=edit_payload)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Career.objects.get(code="CY").name, "Carrera Y Edit")

        # Delete
        resp = self.client.post(reverse("users:career-delete", args=["CY"]))
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Career.objects.filter(code="CY").exists())

    def test_subject_crud_and_assign_professors(self):
        self.client.force_login(self.admin)
        career = make_career("CI")
        subj = make_subject("ALG1", career)
        # Create new subject
        payload = {
            "name": "Álgebra",
            "code": "ALG2",
            "career": career.code,
            "year": 1,
            "category": Subject.Category.OBLIGATORY,
            "period": Subject.Period.FIRST,
            "semanal_hours": 6,
            "description": "desc",
        }
        resp = self.client.post(reverse("users:subject-create"), data=payload)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Subject.objects.filter(code="ALG2").exists())

        # Edit
        payload_edit = payload | {"name": "Álgebra I"}
        resp = self.client.post(reverse("users:subject-edit", args=["ALG2"]), data=payload_edit)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Subject.objects.get(code="ALG2").name, "Álgebra I")

        # Assign professors
        prof_user, prof = make_professor("profX", "55555555")
        resp = self.client.post(
            reverse("users:assign-subject-professors", args=[subj.code]),
            data={"professors": [str(prof.pk)]},
        )
        self.assertEqual(resp.status_code, 302)
        subj.refresh_from_db()
        self.assertIn(prof, subj.professors.all())

        # Delete
        resp = self.client.post(reverse("users:subject-delete", args=["ALG2"]))
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Subject.objects.filter(code="ALG2").exists())

    def test_final_crud_and_assign_professors(self):
        self.client.force_login(self.admin)
        subj = make_subject("MAT1")
        # Create
        payload = {
            "subject": subj.code,
            "date": (date.today() + timedelta(days=7)).isoformat(),
            "location": "Aula 1",
            "duration": "02:00:00",
            "call_number": 1,
            "notes": "1er llamado",
        }
        resp = self.client.post(reverse("users:final-create"), data=payload)
        self.assertEqual(resp.status_code, 302)
        final = FinalExam.objects.latest("id")

        # Edit
        payload_edit = payload | {"location": "Aula 2"}
        resp = self.client.post(reverse("users:final-edit", args=[final.id]), data=payload_edit)
        self.assertEqual(resp.status_code, 302)
        final.refresh_from_db()
        self.assertEqual(final.location, "Aula 2")

        # Assign professors
        _, prof = make_professor("profY", "66666666")
        resp = self.client.post(
            reverse("users:assign-final-professors", args=[final.id]), data={"professors": [str(prof.pk)]}
        )
        self.assertEqual(resp.status_code, 302)
        final.refresh_from_db()
        self.assertIn(prof, final.professors.all())

        # Delete
        resp = self.client.post(reverse("users:final-delete", args=[final.id]))
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(FinalExam.objects.filter(id=final.id).exists())


class StudentViewsTests(TestCase):
    def setUp(self):
        self.student_user, self.student = make_student()
        self.subject = make_subject(career=self.student.career)

    def test_student_dashboard_requires_profile(self):
        # User without profile
        user = CustomUser.objects.create_user(
            username="no_profile",
            password="pass1234",
            role=CustomUser.Role.STUDENT,
            dni="19999999",
        )
        self.client.force_login(user)
        resp = self.client.get(reverse("users:student-dashboard"))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp["Location"], reverse("home"))

    def test_subject_inscribe_flow(self):
        self.client.force_login(self.student_user)
        # GET confirm
        resp = self.client.get(reverse("users:subject-inscribe", args=[self.subject.code]))
        self.assertEqual(resp.status_code, 200)
        # POST create inscription and grade
        resp = self.client.post(reverse("users:subject-inscribe", args=[self.subject.code]))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(SubjectInscription.objects.filter(student=self.student, subject=self.subject).exists())
        self.assertTrue(Grade.objects.filter(student=self.student, subject=self.subject).exists())
        # Second POST idempotent
        resp = self.client.post(reverse("users:subject-inscribe", args=[self.subject.code]))
        self.assertEqual(resp.status_code, 302)

    def test_final_exam_inscribe_requires_regular(self):
        self.client.force_login(self.student_user)
        final = FinalExam.objects.create(
            subject=self.subject,
            date=date.today() + timedelta(days=10),
            location="Aula 1",
            duration="02:00:00",
            call_number=1,
        )
        # No grade -> error message and redirect
        resp = self.client.get(reverse("users:final-inscribe", args=[final.id]))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp["Location"], reverse("users:student-dashboard"))

        # Make regular and POST
        Grade.objects.create(student=self.student, subject=self.subject, status=Grade.StatusSubject.REGULAR)
        resp = self.client.post(reverse("users:final-inscribe", args=[final.id]))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(FinalExamInscription.objects.filter(student=self.student, final_exam=final).exists())

    def test_download_certificate_requires_login_and_student_profile(self):
        # Unauthenticated -> redirect to login
        resp = self.client.get(reverse("users:student-regular-certificate"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/login", resp["Location"])  # login redirect

        # Auth student without linked Student profile -> redirect home
        no_profile_user = CustomUser.objects.create_user(
            username="stud_noprofile",
            password="pass1234",
            role=CustomUser.Role.STUDENT,
            dni="17777777",
        )
        self.client.force_login(no_profile_user)
        resp = self.client.get(reverse("users:student-regular-certificate"))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp["Location"], reverse("home"))

    def test_download_certificate_missing_template_redirects(self):
        # Force login a valid student
        self.client.force_login(self.student_user)

        # Use a temporary BASE_DIR with no template file
        with TemporaryDirectory() as tmpdir:
            with override_settings(BASE_DIR=tmpdir):
                resp = self.client.get(reverse("users:student-regular-certificate"))
                self.assertEqual(resp.status_code, 302)
                self.assertEqual(resp["Location"], reverse("users:student-dashboard"))

    @patch("users.views.DocxTemplate")
    def test_download_certificate_success_returns_docx(self, mock_tpl_cls):
        # Mock DocxTemplate to avoid real file IO and docx processing
        class FakeTpl:
            def __init__(self, *_args, **_kwargs):
                pass

            def render(self, _context):
                return None

            def save(self, dest):
                # Write some bytes to the provided BytesIO
                dest.write(b"PK\x03\x04fake-docx-content")

        mock_tpl_cls.return_value = FakeTpl()

        # Ensure logged in as valid student
        self.client.force_login(self.student_user)
        resp = self.client.get(reverse("users:student-regular-certificate"))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp["Content-Type"],
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
        content_disp = resp["Content-Disposition"]
        ok = (
            "attachment; filename=\"certificado-regular-" in content_disp
            or "attachment; filename=\"certificado-regular-stud-" in content_disp
        )
        self.assertTrue(ok)
        self.assertTrue(len(resp.content) > 0)


class ProfessorViewsTests(TestCase):
    def setUp(self):
        self.prof_user, self.prof = make_professor()
        self.student_user, self.student = make_student(dni="12223334")
        self.subject = make_subject(career=self.student.career)
        # Assign professor to subject
        self.prof.subjects.add(self.subject)

    def test_professor_dashboard_requires_profile(self):
        user = CustomUser.objects.create_user(
            username="no_prof_profile",
            password="pass1234",
            role=CustomUser.Role.PROFESSOR,
            dni="18888888",
        )
        self.client.force_login(user)
        resp = self.client.get(reverse("users:professor-dashboard"))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp["Location"], reverse("home"))

    def test_grade_list_creates_missing_grades(self):
        SubjectInscription.objects.create(student=self.student, subject=self.subject)
        self.client.force_login(self.prof_user)
        resp = self.client.get(reverse("users:grade-list", args=[self.subject.code]))
        self.assertEqual(resp.status_code, 200)
        # Grade should be auto-created
        self.assertTrue(Grade.objects.filter(student=self.student, subject=self.subject).exists())

    def test_grade_edit_permissions_and_update(self):
        # Create grade and inscription
        SubjectInscription.objects.create(student=self.student, subject=self.subject)
        grade = Grade.objects.create(student=self.student, subject=self.subject)
        # Another subject not assigned to professor
        other_subject = make_subject("HIS1", self.student.career)
        grade_other = Grade.objects.create(student=self.student, subject=other_subject)

        self.client.force_login(self.prof_user)
        # Cannot edit not assigned
        resp = self.client.post(reverse("users:grade-edit", args=[grade_other.id]), data={"final_grade": 7})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp["Location"], reverse("users:professor-dashboard"))

        # Can edit assigned and update_status auto-applies
        resp = self.client.post(
            reverse("users:grade-edit", args=[grade.id]),
            data={"promotion_grade": 8, "final_grade": 7, "status": Grade.StatusSubject.REGULAR},
        )
        self.assertEqual(resp.status_code, 302)
        grade.refresh_from_db()
    # Since status wasn't changed explicitly (remains REGULAR),
    # update_status should set PROMOTED for final_grade >= 6
        self.assertEqual(grade.status, Grade.StatusSubject.PROMOTED)

    def test_professor_final_inscriptions_list(self):
        final = FinalExam.objects.create(
            subject=self.subject,
            date=date.today() + timedelta(days=7),
            location="Aula 1",
            duration="02:00:00",
            call_number=1,
        )
        # Assign professor to final and create one inscription
        self.prof.final_exams.add(final)
        FinalExamInscription.objects.create(student=self.student, final_exam=final)
        self.client.force_login(self.prof_user)
        resp = self.client.get(reverse("users:professor-final-inscriptions", args=[final.id]))
        self.assertEqual(resp.status_code, 200)
