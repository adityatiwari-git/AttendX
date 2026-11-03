from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms import modelformset_factory
from django import forms
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import User
from academics.models import Subject
from .models import AttendanceRecord, ClassSession
class ClassSessionForm(forms.ModelForm):
    class Meta:
        model = ClassSession
        fields = ("subject","session_date","topic","status")
        widgets = {"session_date":forms.DateInput(attrs={"type":"date"})}
@login_required
def mark_attendance(request):
    if request.user.role != User.Role.FACULTY and not request.user.is_superuser: return HttpResponseForbidden()
    subjects = Subject.objects.all() if request.user.is_superuser else Subject.objects.filter(faculty=request.user)
    form = ClassSessionForm(request.POST or None)
    form.fields["subject"].queryset = subjects
    if request.method == "POST" and form.is_valid():
        session = form.save()
        students = User.objects.filter(enrollments__subject=session.subject,role=User.Role.STUDENT).distinct()
        with transaction.atomic():
            for student in students:
                AttendanceRecord.objects.update_or_create(session=session,student=student,defaults={"status":"ABSENT","marked_by":request.user})
        messages.success(request,"Session created. Review attendance records.")
        return redirect("session_detail",session_id=session.pk)
    return render(request,"attendance/mark.html",{"form":form})
@login_required
def session_detail(request,session_id):
    session = get_object_or_404(ClassSession.objects.select_related("subject"),pk=session_id)
    if request.user.role == User.Role.FACULTY and session.subject.faculty_id != request.user.id: return HttpResponseForbidden()
    if request.user.role not in [User.Role.FACULTY,User.Role.ADMIN] and not request.user.is_superuser: return HttpResponseForbidden()
    FormSet = modelformset_factory(AttendanceRecord,fields=("status",),extra=0)
    qs = session.records.select_related("student")
    formset = FormSet(request.POST or None,queryset=qs)
    if request.method == "POST" and formset.is_valid():
        formset.save()
        messages.success(request,"Attendance updated.")
        return redirect("session_detail",session_id=session.pk)
    return render(request,"attendance/session_detail.html",{"session":session,"formset":formset})
