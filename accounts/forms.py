from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User


class RoleAuthenticationForm(AuthenticationForm):
    # The Master Admin is intentionally not exposed as a selectable login role.
    role = forms.ChoiceField(
        choices=(
            (User.Role.STUDENT, "Student"),
            (User.Role.FACULTY, "Faculty"),
        ),
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Continue as",
    )

    def clean(self):
        cleaned_data = super().clean()
        selected_role = cleaned_data.get("role")
        user = self.get_user()
        if user and selected_role:
            # A valid Master Admin credential works from either visible login choice.
            if user.role != User.Role.ADMIN and user.role != selected_role:
                raise forms.ValidationError(
                    "No account was found for the selected login type. "
                    "Check your credentials and selected role."
                )
        return cleaned_data
