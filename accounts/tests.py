from datetime import date

from django.test import TestCase
from django.urls import reverse

from app.models import CustomUser, Student, Professor, Administrator


class AccountsViewsTests(TestCase):
    def setUp(self):
        self.student_user = CustomUser.objects.create_user(
            username="stud1",
            password="pass1234",
            role="student",
            dni="10000001",
        )
        Student.objects.create(
            student_id="S-1",
            user=self.student_user,
            career=None,
            enrollment_date=date(2020, 1, 1),
        )

        self.prof_user = CustomUser.objects.create_user(
            username="prof1",
            password="pass1234",
            role="professor",
            dni="10000002",
        )
        Professor.objects.create(
            professor_id="P-1",
            user=self.prof_user,
            degree="Ing.",
            hire_date=date(2019, 1, 1),
            category="titular",
        )

        self.admin_user = CustomUser.objects.create_user(
            username="admin1",
            password="pass1234",
            role="administrator",
            dni="10000003",
        )
        Administrator.objects.create(
            administrator_id="A-1",
            user=self.admin_user,
            position="SysAdmin",
            hire_date=date(2018, 1, 1),
        )

    def test_login_get_renders_form(self):
        resp = self.client.get(reverse("login"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'name="username"')
        self.assertContains(resp, 'name="password"')

    def test_login_invalid_credentials_shows_error(self):
        resp = self.client.post(reverse("login"), {
            "username": "unknown",
            "password": "badpass",
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Incorrect username or password.")

    def test_login_student_redirects_to_student_dashboard(self):
        resp = self.client.post(reverse("login"), {
            "username": "stud1",
            "password": "pass1234",
        })
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(reverse("users:student-dashboard").endswith("/student/dashboard/"))
        self.assertIn("/student/dashboard/", resp["Location"])  # don't follow to avoid dashboard dependency

    def test_login_professor_redirects_to_professor_dashboard(self):
        resp = self.client.post(reverse("login"), {
            "username": "prof1",
            "password": "pass1234",
        })
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/professor/dashboard/", resp["Location"])  # don't follow

    def test_login_admin_redirects_to_admin_dashboard(self):
        resp = self.client.post(reverse("login"), {
            "username": "admin1",
            "password": "pass1234",
        })
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/admin/dashboard/", resp["Location"])  # don't follow

    def test_login_respects_next_parameter(self):
        next_url = "/some/protected/path/"
        url = f"{reverse('login')}?next={next_url}"
        resp = self.client.post(url, {
            "username": "stud1",
            "password": "pass1234",
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp["Location"], next_url)

    def test_authenticated_user_visiting_login_redirects_by_role(self):
        # Student
        self.client.force_login(self.student_user)
        resp = self.client.get(reverse("login"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/student/dashboard/", resp["Location"])  # don't follow
        # Logout to isolate next check
        self.client.logout()

        # Professor
        self.client.force_login(self.prof_user)
        resp = self.client.get(reverse("login"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/professor/dashboard/", resp["Location"])  # don't follow
        self.client.logout()

        # Administrator
        self.client.force_login(self.admin_user)
        resp = self.client.get(reverse("login"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/admin/dashboard/", resp["Location"])  # don't follow

    def test_logout_redirects_home(self):
        self.client.force_login(self.student_user)
        resp = self.client.get(reverse("logout"))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp["Location"], reverse("home"))
