from django.contrib.auth.password_validation import validate_password
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Securely create the single AttendX Master Admin account."

    def handle(self, *args, **options):
        User = get_user_model()
        if User.objects.filter(role=User.Role.ADMIN).exists():
            raise CommandError("A Master Admin already exists. This command will not create another one.")

        username = input("Master Admin username: ").strip()
        if not username:
            raise CommandError("Username cannot be empty.")
        if User.objects.filter(username=username).exists():
            raise CommandError("That username is already in use.")

        email = input("Master Admin email (optional): ").strip()
        password = self._prompt_password()
        try:
            validate_password(password)
        except Exception as exc:
            raise CommandError(str(exc)) from exc

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=User.Role.ADMIN,
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        self.stdout.write(self.style.SUCCESS(
            f"Master Admin '{user.username}' created. Store the credentials securely."
        ))

    def _prompt_password(self):
        from getpass import getpass
        first = getpass("Master Admin password (input hidden): ")
        second = getpass("Confirm password: ")
        if first != second:
            raise CommandError("Passwords do not match.")
        if not first:
            raise CommandError("Password cannot be empty.")
        return first
