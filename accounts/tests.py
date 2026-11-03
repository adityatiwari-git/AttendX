from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from .forms import RegistrationForm, RoleAuthenticationForm
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


class LoginRoleRoutingTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="masteradmin", password="StrongPass!2026",
            role=User.Role.ADMIN, is_staff=True, is_superuser=True,
        )
        self.student = User.objects.create_user(
            username="student1", password="StrongPass!2026", role=User.Role.STUDENT,
        )
        self.faculty = User.objects.create_user(
            username="faculty1", password="StrongPass!2026", role=User.Role.FACULTY,
        )

    def _form(self, username, role):
        return RoleAuthenticationForm(data={
            "username": username,
            "password": "StrongPass!2026",
            "role": role,
        })

    def test_admin_can_sign_in_from_student_choice(self):
        form = self._form("masteradmin", User.Role.STUDENT)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.get_user(), self.admin)

    def test_admin_can_sign_in_from_faculty_choice(self):
        form = self._form("masteradmin", User.Role.FACULTY)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.get_user(), self.admin)

    def test_student_cannot_choose_faculty_workspace(self):
        form = self._form("student1", User.Role.FACULTY)
        self.assertFalse(form.is_valid())

    def test_faculty_cannot_choose_student_workspace(self):
        form = self._form("faculty1", User.Role.STUDENT)
        self.assertFalse(form.is_valid())

    def test_admin_is_not_a_visible_login_choice(self):
        form = RoleAuthenticationForm()
        self.assertEqual(
            [value for value, _label in form.fields["role"].choices],
            [User.Role.STUDENT, User.Role.FACULTY],
        )


class MasterAdminProtectionTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="masteradmin", password="StrongPass!2026",
            role=User.Role.ADMIN, is_staff=True, is_superuser=True,
        )

    def test_second_master_admin_is_rejected(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                User.objects.create_user(
                    username="secondadmin", password="StrongPass!2026",
                    role=User.Role.ADMIN,
                )

    def test_master_admin_cannot_be_demoted(self):
        self.admin.role = User.Role.FACULTY
        with self.assertRaises(ValidationError):
            self.admin.save()

    def test_master_admin_cannot_be_deactivated(self):
        self.admin.is_active = False
        with self.assertRaises(ValidationError):
            self.admin.save()

    def test_master_admin_cannot_be_deleted(self):
        with self.assertRaises(ValidationError):
            self.admin.delete()

    def test_non_admin_cannot_keep_staff_or_superuser_flags(self):
        user = User.objects.create_user(
            username="ordinary", password="StrongPass!2026",
            role=User.Role.FACULTY, is_staff=True, is_superuser=True,
        )
        user.refresh_from_db()
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_admin_admin_form_does_not_offer_admin_role_for_new_accounts(self):
        from .admin import AttendXUserCreationForm
        form = AttendXUserCreationForm()
        self.assertEqual(
            [value for value, _label in form.fields["role"].choices],
            [User.Role.FACULTY, User.Role.STUDENT],
        )
