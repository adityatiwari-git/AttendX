from django.contrib import admin
from .models import AcademicBatch, Course, Department, Enrollment, FacultySubjectAssignment, StudentProfile, Subject, TimetableEntry


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "department", "duration_years")
    list_filter = ("department",)
    search_fields = ("name", "code")


@admin.register(AcademicBatch)
class AcademicBatchAdmin(admin.ModelAdmin):
    list_display = ("name", "course", "admission_year", "graduation_year", "academic_year")
    list_filter = ("course", "admission_year")


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("student", "batch", "current_semester", "roll_number")
    list_filter = ("batch__course", "current_semester")
    search_fields = ("student__username", "student__email", "roll_number")


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "course", "semester", "faculty")
    list_filter = ("course__department", "course", "semester")
    search_fields = ("name", "code")


@admin.register(FacultySubjectAssignment)
class FacultySubjectAssignmentAdmin(admin.ModelAdmin):
    list_display = ("faculty", "subject", "academic_year", "is_coordinator")
    list_filter = ("subject__course__department", "subject__course", "subject__semester", "academic_year")
    search_fields = ("faculty__username", "faculty__email", "subject__name", "subject__code")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "academic_year")
    list_filter = ("subject__course__department", "subject__course", "subject__semester", "academic_year")
    search_fields = ("student__username", "student__email", "subject__name")


@admin.register(TimetableEntry)
class TimetableEntryAdmin(admin.ModelAdmin):
    list_display = ("batch", "subject", "faculty", "weekday", "start_time", "end_time", "room")
    list_filter = ("batch__course", "batch", "weekday")
