from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrator"
        FACULTY = "FACULTY", "Faculty"
        STUDENT = "STUDENT", "Student"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("role",),
                condition=Q(role="ADMIN"),
                name="accounts_single_master_admin",
            )
        ]

    def save(self, *args, **kwargs):
        if self.role == self.Role.ADMIN:
            self.is_staff = True
            self.is_superuser = True
            self.is_active = True
        else:
            # No non-admin role may carry Django's privileged account flags.
            self.is_staff = False
            self.is_superuser = False

        if self.pk:
            previous = type(self).objects.filter(pk=self.pk).values(
                "role", "is_staff", "is_superuser", "is_active"
            ).first()
            if previous and previous["role"] == self.Role.ADMIN:
                protected_state = (
                    self.role == self.Role.ADMIN
                    and self.is_staff
                    and self.is_superuser
                    and self.is_active
                )
                if not protected_state:
                    raise ValidationError(
                        "The Master Admin account cannot be demoted, deactivated, or stripped of administrator privileges."
                    )
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.role == self.Role.ADMIN:
            raise ValidationError("The Master Admin account cannot be deleted.")
        return super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
