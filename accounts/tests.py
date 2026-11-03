from django.test import TestCase
from django.urls import reverse
from .models import User

class AccountFlowTests(TestCase):
    def test_public_registration_creates_student_only(self):
        response = self.client.post(reverse("register"), {
            "username":"learner01","first_name":"Demo","last_name":"Student",
            "email":"learner@example.test","password1":"StrongPass!9284",
            "password2":"StrongPass!9284","role":"ADMIN",
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username="learner01")
        self.assertEqual(user.role, User.Role.STUDENT)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
