from django.conf import settings
from django.db import models
class Department(models.Model):
    name = models.CharField(max_length=120, unique=True)
    code = models.CharField(max_length=12, unique=True)
    def __str__(self): return self.name
class Course(models.Model):
    department = models.ForeignKey(Department,on_delete=models.PROTECT,related_name="courses")
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=20,unique=True)
    duration_years = models.PositiveSmallIntegerField(default=4)
    def __str__(self): return self.name
class Subject(models.Model):
    course = models.ForeignKey(Course,on_delete=models.PROTECT,related_name="subjects")
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=20)
    semester = models.PositiveSmallIntegerField()
    faculty = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="teaching_subjects",limit_choices_to={"role":"FACULTY"})
    class Meta:
        constraints = [models.UniqueConstraint(fields=["course","code","semester"],name="unique_course_subject_semester")]
    def __str__(self): return f"{self.code} — {self.name}"
class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="enrollments",limit_choices_to={"role":"STUDENT"})
    subject = models.ForeignKey(Subject,on_delete=models.PROTECT,related_name="enrollments")
    academic_year = models.CharField(max_length=9)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["student","subject","academic_year"],name="unique_student_subject_year")]
    def __str__(self): return f"{self.student} — {self.subject}"
