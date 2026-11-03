from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class ProtectedUserQuerySet(models.QuerySet):
    def delete(self):
        # Bulk deletion must never remove the institutional Master Admin.
        return models.QuerySet.delete(self.exclude(role="ADMIN"))


class AttendXUserManager(UserManager.from_queryset(ProtectedUserQuerySet)):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields["role"] = "ADMIN"
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
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
            models.UniqueConstraint(fields=("role",), condition=Q(role="ADMIN"), name="accounts_single_master_admin")
        ]

    def save(self, *args, **kwargs):
        if self.pk:
            previous = type(self).objects.filter(pk=self.pk).values("role").first()
            if previous and previous["role"] == self.Role.ADMIN and self.role != self.Role.ADMIN:
                raise ValidationError("The Master Admin role cannot be removed or changed.")
        if self.role == self.Role.ADMIN:
            self.is_staff = True
            self.is_superuser = True
        elif self.is_superuser:
            raise ValidationError("Only the Master Admin account may be a superuser.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.role == self.Role.ADMIN:
            raise ValidationError("The Master Admin account cannot be deleted.")
        return super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
