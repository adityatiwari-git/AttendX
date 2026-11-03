from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.models import User
from academics.models import Subject
from attendance.models import AttendanceRecord
def home(request):
    return render(request, "core/home.html")
@login_required
def dashboard(request):
    user = request.user
    if user.role == User.Role.STUDENT:
        records = AttendanceRecord.objects.filter(student=user).select_related("session__subject")
        total = records.count()
        present = records.filter(status="PRESENT").count()
        return render(request,"dashboards/student.html",{"total":total,"present":present,"percentage":round(100*present/total,1) if total else 0,"recent":records[:10]})
    if user.role == User.Role.FACULTY:
        subjects = Subject.objects.filter(faculty=user)
        return render(request,"dashboards/faculty.html",{"subjects":subjects,"session_count":sum(s.sessions.count() for s in subjects)})
    return render(request,"dashboards/admin.html",{"students":User.objects.filter(role="STUDENT").count(),"faculty":User.objects.filter(role="FACULTY").count(),"subjects":Subject.objects.count()})
