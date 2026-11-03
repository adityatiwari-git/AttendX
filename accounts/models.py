from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class ProtectedUserQuerySet(models.QuerySet):
    def delete(self):
        if self.filter(role="ADMIN").exists():
            raise ValidationError("The Master Admin account cannot be deleted.")
        return super().delete()


class AttendXUserManager(UserManager.from_queryset(ProtectedUserQuerySet)):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields["role"] = "ADMIN"
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
        extra_fields["is_active"] = True
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrator"
        FACULTY = "FACULTY", "Faculty"
        STUDENT = "STUDENT", "Student"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)
    objects = AttendXUserManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("role",),
                condition=Q(role="ADMIN"),
                name="accounts_single_master_admin",
            )
        ]

    def save(self, *args, **kwargs):
        if self.pk:
            previous = type(self).objects.filter(pk=self.pk).values(
                "role", "is_staff", "is_superuser", "is_active"
            ).first()
            if previous and previous["role"] == self.Role.ADMIN:
                if not (
                    self.role == self.Role.ADMIN
                    and self.is_staff
                    and self.is_superuser
                    and self.is_active
                ):
                    raise ValidationError(
                        "The Master Admin account cannot be demoted, deactivated, or stripped of administrator privileges."
                    )

        if self.role == self.Role.ADMIN:
            self.is_staff = True
            self.is_superuser = True
            self.is_active = True
        else:
            self.is_staff = False
            self.is_superuser = False

        update_fields = kwargs.get("update_fields")
        if update_fields is not None:
            kwargs["update_fields"] = set(update_fields) | {"is_staff", "is_superuser"}
            if self.role == self.Role.ADMIN:
                kwargs["update_fields"].add("is_active")
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.role == self.Role.ADMIN:
            raise ValidationError("The Master Admin account cannot be deleted.")
        return super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
