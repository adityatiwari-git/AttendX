from django.test import TestCase
from django.urls import reverse
from .forms import RegistrationForm
from .models import User


class RegistrationRoleSecurityTests(TestCase):
    def test_public_registration_always_creates_student(self):
        form = RegistrationForm(data={
            "username": "newstudent",
            "first_name": "New",
            "last_name": "Student",
            "email": "student@example.com",
            "password1": "StrongPass!2026",
            "password2": "StrongPass!2026",
        })
        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()
        self.assertEqual(user.role, User.Role.STUDENT)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_student_cannot_open_admin_console(self):
        user = User.objects.create_user(username="learner", password="StrongPass!2026", role=User.Role.STUDENT)
        self.client.force_login(user)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 302)
