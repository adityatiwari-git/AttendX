from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class AttendXUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=((User.Role.FACULTY, "Faculty"), (User.Role.STUDENT, "Student")),
        required=True,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "first_name", "last_name", "role")


class AttendXUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.role == User.Role.ADMIN:
            self.fields["role"].disabled = True
        else:
            self.fields["role"].choices = (
                (User.Role.FACULTY, "Faculty"),
                (User.Role.STUDENT, "Student"),
            )


@admin.register(User)
class AttendXUserAdmin(UserAdmin):
    form = AttendXUserChangeForm
    add_form = AttendXUserCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        ("AttendX role", {"fields": ("role",)}),
        ("Account status", {"fields": ("is_active", "date_joined")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("username", "email", "first_name", "last_name", "role", "password1", "password2")}),
    )
    list_display = ("username", "email", "first_name", "last_name", "role", "is_active")
    list_filter = ("role", "is_active")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.role == User.Role.ADMIN:
            return ("role", "is_active", "date_joined")
        return ("date_joined",)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.role == User.Role.ADMIN:
            return False
        return super().has_delete_permission(request, obj)

    def save_model(self, request, obj, form, change):
        if obj.role == User.Role.ADMIN:
            obj.is_staff = True
            obj.is_superuser = True
            obj.is_active = True
        else:
            obj.is_staff = False
            obj.is_superuser = False
        super().save_model(request, obj, form, change)
