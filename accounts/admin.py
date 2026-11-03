from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class AttendXUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("AttendX role", {"fields": ("role",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("AttendX role", {"fields": ("role",)}),)
    list_display = ("username", "email", "first_name", "last_name", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff")

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if "role" in form.base_fields:
            if obj and obj.role == User.Role.ADMIN:
                form.base_fields["role"].disabled = True
            else:
                form.base_fields["role"].choices = (
                    (User.Role.STUDENT, "Student"),
                    (User.Role.FACULTY, "Faculty"),
                )
        return form

    def save_model(self, request, obj, form, change):
        if obj.role != User.Role.ADMIN:
            obj.is_staff = False
            obj.is_superuser = False
        super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.role == User.Role.ADMIN:
            return False
        return super().has_delete_permission(request, obj)

    def delete_model(self, request, obj):
        if obj.role != User.Role.ADMIN:
            super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        queryset.exclude(role=User.Role.ADMIN).delete()
