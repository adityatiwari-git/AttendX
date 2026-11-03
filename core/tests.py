from django.test import TestCase
from django.urls import reverse
from accounts.models import User

class DashboardTests(TestCase):
    def test_home_is_public(self):
        self.assertEqual(self.client.get(reverse("home")).status_code, 200)

    def test_student_dashboard_is_available_after_login(self):
        user = User.objects.create_user(username="student1", password="TestPass!12345", role=User.Role.STUDENT)
        self.client.force_login(user)
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Student dashboard")
