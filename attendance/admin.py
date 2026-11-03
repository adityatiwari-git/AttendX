from django.contrib import admin
from .models import AttendanceConcern, AttendanceRecord, ClassSession


@admin.register(ClassSession)
class ClassSessionAdmin(admin.ModelAdmin):
    list_display = ("subject", "session_date", "status")
    list_filter = ("status", "session_date")
    search_fields = ("subject__name", "topic")


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ("student", "session", "status", "marked_by")
    list_filter = ("status", "session__session_date")
    search_fields = ("student__username", "student__email", "session__subject__name")


@admin.register(AttendanceConcern)
class AttendanceConcernAdmin(admin.ModelAdmin):
    list_display = ("student", "record", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("student__username", "message", "record__session__subject__name")
    readonly_fields = ("created_at", "updated_at")
