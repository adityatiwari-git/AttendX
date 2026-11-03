from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User


class RoleAuthenticationForm(AuthenticationForm):
    role = forms.ChoiceField(
        choices=User.Role.choices,
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Sign in as",
    )

    def clean(self):
        cleaned_data = super().clean()
        selected_role = cleaned_data.get("role")
        user = self.get_user()
        if user and selected_role:
            valid_admin = selected_role == User.Role.ADMIN and (user.role == User.Role.ADMIN or user.is_superuser)
            if not valid_admin and user.role != selected_role:
                raise forms.ValidationError("This account does not have access to the selected workspace. Choose the correct role or contact your administrator.")
        return cleaned_data
