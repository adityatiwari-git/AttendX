from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class AttendXUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("AttendX role", {"fields": ("role",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("AttendX role", {"fields": ("role",)}),)
    list_display = ("username", "email", "first_name", "last_name", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff")

    def save_model(self, request, obj, form, change):
        if obj.role == User.Role.ADMIN:
            # ADMIN is the trusted, full-control institutional role.
            obj.is_staff = True
            obj.is_superuser = True
        elif not obj.is_superuser:
            obj.is_staff = False
        super().save_model(request, obj, form, change)
