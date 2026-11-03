from django.contrib import admin
from .models import Department, Course, Subject, Enrollment
admin.site.register([Department,Course,Subject,Enrollment])
