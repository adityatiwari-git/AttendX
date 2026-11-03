from django.db import migrations, models
from django.db.models import Q


# Keep one existing privileged account as the Master Admin; preserve other user records.
def consolidate_master_admin(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    alias = schema_editor.connection.alias
    users = User.objects.using(alias).all().order_by("id")
    designated = users.filter(role="ADMIN").first()
    if designated is None:
        designated = users.filter(is_superuser=True).first()

    for user in users.iterator():
        if designated and user.pk == designated.pk:
            User.objects.using(alias).filter(pk=user.pk).update(
                role="ADMIN", is_staff=True, is_superuser=True, is_active=True
            )
        elif user.role == "ADMIN" or user.is_superuser or user.is_staff:
            # Keep existing accounts and passwords, but remove unintended
            # administrative privileges before enforcing the single-admin rule.
            fallback_role = user.role if user.role in ("FACULTY", "STUDENT") else "STUDENT"
            User.objects.using(alias).filter(pk=user.pk).update(
                role=fallback_role, is_staff=False, is_superuser=False
            )


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(consolidate_master_admin, migrations.RunPython.noop),
        migrations.AddConstraint(
            model_name="user",
            constraint=models.UniqueConstraint(
                fields=("role",),
                condition=Q(role="ADMIN"),
                name="accounts_single_master_admin",
            ),
        ),
    ]
