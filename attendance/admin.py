from django.contrib import admin
from .models import ClassSession, AttendanceRecord
@admin.register(ClassSession)
class ClassSessionAdmin(admin.ModelAdmin):
    list_display = ("subject","session_date","status")
    list_filter = ("status","session_date")
@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ("student","session","status","marked_by")
    list_filter = ("status",)
