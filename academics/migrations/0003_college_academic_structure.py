# Generated for the AttendX college-wide academic structure.
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("academics", "0002_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="subject",
            name="faculty",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                related_name="legacy_teaching_subjects",
                limit_choices_to={"role": "FACULTY"},
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="AcademicBatch",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=60, help_text="e.g. 2025–2029")),
                ("admission_year", models.PositiveSmallIntegerField()),
                ("graduation_year", models.PositiveSmallIntegerField()),
                ("academic_year", models.CharField(max_length=9, help_text="e.g. 2026-2027")),
                ("course", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="batches", to="academics.course")),
            ],
            options={"ordering": ("-admission_year", "course__name")},
        ),
        migrations.CreateModel(
            name="FacultySubjectAssignment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("academic_year", models.CharField(blank=True, max_length=9)),
                ("is_coordinator", models.BooleanField(default=False)),
                ("faculty", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="subject_assignments", limit_choices_to={"role": "FACULTY"}, to=settings.AUTH_USER_MODEL)),
                ("subject", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="faculty_assignments", to="academics.subject")),
            ],
        ),
        migrations.CreateModel(
            name="StudentProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("current_semester", models.PositiveSmallIntegerField(default=1)),
                ("roll_number", models.CharField(blank=True, max_length=40)),
                ("batch", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="students", to="academics.academicbatch")),
                ("student", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="academic_profile", limit_choices_to={"role": "STUDENT"}, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="TimetableEntry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("weekday", models.PositiveSmallIntegerField(choices=[(0,"Monday"),(1,"Tuesday"),(2,"Wednesday"),(3,"Thursday"),(4,"Friday"),(5,"Saturday"),(6,"Sunday")])),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
                ("room", models.CharField(blank=True, max_length=60)),
                ("batch", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="timetable_entries", to="academics.academicbatch")),
                ("faculty", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="timetable_entries", limit_choices_to={"role": "FACULTY"}, to=settings.AUTH_USER_MODEL)),
                ("subject", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="timetable_entries", to="academics.subject")),
            ],
            options={"ordering": ("weekday", "start_time")},
        ),
        migrations.AddConstraint(model_name="academicbatch", constraint=models.UniqueConstraint(fields=("course","admission_year"), name="unique_course_admission_batch")),
        migrations.AddConstraint(model_name="facultysubjectassignment", constraint=models.UniqueConstraint(fields=("faculty","subject","academic_year"), name="unique_faculty_subject_year")),
        migrations.AddConstraint(model_name="timetableentry", constraint=models.UniqueConstraint(fields=("batch","weekday","start_time","room"), name="unique_batch_timetable_slot")),
    ]
