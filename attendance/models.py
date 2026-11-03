from django.conf import settings
from django.db import models


class ClassSession(models.Model):
    class Status(models.TextChoices):
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    subject = models.ForeignKey("academics.Subject", on_delete=models.PROTECT, related_name="sessions")
    session_date = models.DateField()
    topic = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.COMPLETED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-session_date", "-id")

    def __str__(self):
        return f"{self.subject} — {self.session_date}"


class AttendanceRecord(models.Model):
    class Status(models.TextChoices):
        PRESENT = "PRESENT", "Present"
        ABSENT = "ABSENT", "Absent"
        LATE = "LATE", "Late"

    session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, related_name="records")
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="attendance_records", limit_choices_to={"role": "STUDENT"})
    status = models.CharField(max_length=8, choices=Status.choices, default=Status.ABSENT)
    marked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="marked_attendance_records")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("session__session_date", "student__username")
        constraints = [models.UniqueConstraint(fields=("session", "student"), name="unique_attendance_per_student_session")]

    def __str__(self):
        return f"{self.student} — {self.session} — {self.get_status_display()}"


class AttendanceConcern(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        REVIEWING = "REVIEWING", "Under review"
        RESOLVED = "RESOLVED", "Resolved"
        DECLINED = "DECLINED", "Declined"

    record = models.ForeignKey(AttendanceRecord, on_delete=models.CASCADE, related_name="concerns")
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="attendance_concerns")
    message = models.TextField(max_length=1000)
    faculty_response = models.TextField(max_length=1000, blank=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"Concern by {self.student} for {self.record}"
