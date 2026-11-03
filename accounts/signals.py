from django.core.exceptions import ValidationError
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import User


@receiver(pre_delete, sender=User)
def prevent_master_admin_bulk_delete(sender, instance, **kwargs):
    if instance.role == User.Role.ADMIN:
        raise ValidationError("The Master Admin account cannot be deleted.")
