from django.conf import settings
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=120, unique=True)
    code = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="courses")
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=20, unique=True)
    duration_years = models.PositiveSmallIntegerField(default=4)

    def __str__(self):
        return self.name


class AcademicBatch(models.Model):
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name="batches")
    name = models.CharField(max_length=60, help_text="e.g. 2025–2029")
    admission_year = models.PositiveSmallIntegerField()
    graduation_year = models.PositiveSmallIntegerField()
    academic_year = models.CharField(max_length=9, help_text="e.g. 2026-2027")

    class Meta:
        ordering = ("-admission_year", "course__name")
        constraints = [models.UniqueConstraint(fields=("course", "admission_year"), name="unique_course_admission_batch")]

    def __str__(self):
        return f"{self.course.name} · {self.name}"


class StudentProfile(models.Model):
    student = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="academic_profile", limit_choices_to={"role": "STUDENT"})
    batch = models.ForeignKey(AcademicBatch, on_delete=models.PROTECT, related_name="students")
    current_semester = models.PositiveSmallIntegerField(default=1)
    roll_number = models.CharField(max_length=40, blank=True)

    def __str__(self):
        return f"{self.student} · {self.batch}"


class Subject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name="subjects")
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=20)
    semester = models.PositiveSmallIntegerField()
    faculty = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="legacy_teaching_subjects", limit_choices_to={"role": "FACULTY"}, null=True, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["course", "code", "semester"], name="unique_course_subject_semester")]
        ordering = ("semester", "code")

    @property
    def instructors(self):
        return [assignment.faculty for assignment in self.faculty_assignments.select_related("faculty")]

    def __str__(self):
        return f"{self.code} — {self.name}"


class FacultySubjectAssignment(models.Model):
    faculty = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subject_assignments", limit_choices_to={"role": "FACULTY"})
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="faculty_assignments")
    academic_year = models.CharField(max_length=9, blank=True)
    is_coordinator = models.BooleanField(default=False)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("faculty", "subject", "academic_year"), name="unique_faculty_subject_year")]

    def __str__(self):
        return f"{self.faculty} → {self.subject}"


class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="enrollments", limit_choices_to={"role": "STUDENT"})
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, related_name="enrollments")
    academic_year = models.CharField(max_length=9)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["student", "subject", "academic_year"], name="unique_student_subject_year")]
        ordering = ("subject__semester", "subject__code")

    def __str__(self):
        return f"{self.student} — {self.subject}"


class TimetableEntry(models.Model):
    class Weekday(models.IntegerChoices):
        MONDAY = 0, "Monday"
        TUESDAY = 1, "Tuesday"
        WEDNESDAY = 2, "Wednesday"
        THURSDAY = 3, "Thursday"
        FRIDAY = 4, "Friday"
        SATURDAY = 5, "Saturday"
        SUNDAY = 6, "Sunday"

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="timetable_entries")
    faculty = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="timetable_entries", limit_choices_to={"role": "FACULTY"})
    batch = models.ForeignKey(AcademicBatch, on_delete=models.CASCADE, related_name="timetable_entries")
    weekday = models.PositiveSmallIntegerField(choices=Weekday.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=60, blank=True)

    class Meta:
        ordering = ("weekday", "start_time")
        constraints = [models.UniqueConstraint(fields=("batch", "weekday", "start_time", "room"), name="unique_batch_timetable_slot")]

    def __str__(self):
        return f"{self.get_weekday_display()} {self.start_time} · {self.subject}"
