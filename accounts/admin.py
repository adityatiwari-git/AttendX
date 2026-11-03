from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
@admin.register(User)
class AttendXUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("AttendX role", {"fields": ("role",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("AttendX role", {"fields": ("role",)}),)
    list_display = ("username","email","first_name","last_name","role","is_active")
    list_filter = ("role","is_active")
