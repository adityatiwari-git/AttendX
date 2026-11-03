from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.forms import modelformset_factory
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import User
from academics.models import FacultySubjectAssignment, Subject
from .models import AttendanceConcern, AttendanceRecord, ClassSession


class ClassSessionForm(forms.ModelForm):
    class Meta:
        model = ClassSession
        fields = ("subject", "session_date", "topic", "status")
        widgets = {"session_date": forms.DateInput(attrs={"type": "date"})}


class AttendanceConcernForm(forms.ModelForm):
    class Meta:
        model = AttendanceConcern
        fields = ("message",)
        widgets = {"message": forms.Textarea(attrs={"rows": 3, "placeholder": "Explain why you believe this attendance entry needs review..."})}


class ConcernReviewForm(forms.ModelForm):
    class Meta:
        model = AttendanceConcern
        fields = ("status", "faculty_response")
        widgets = {"faculty_response": forms.Textarea(attrs={"rows": 2, "placeholder": "Add a response for the student..."})}


def faculty_can_teach(user, subject):
    return user.is_superuser or user.role == User.Role.ADMIN or (
        user.role == User.Role.FACULTY and (
            subject.faculty_id == user.id or
            FacultySubjectAssignment.objects.filter(faculty=user, subject=subject).exists()
        )
    )


@login_required
def mark_attendance(request):
    if request.user.role not in [User.Role.FACULTY, User.Role.ADMIN] and not request.user.is_superuser:
        return HttpResponseForbidden()
    subjects = Subject.objects.all() if request.user.role == User.Role.ADMIN or request.user.is_superuser else Subject.objects.filter(
        Q(faculty=request.user) | Q(faculty_assignments__faculty=request.user)
    ).distinct()
    form = ClassSessionForm(request.POST or None)
    form.fields["subject"].queryset = subjects
    if request.method == "POST" and form.is_valid():
        session = form.save(commit=False)
        session.faculty = request.user if request.user.role == User.Role.FACULTY else None
        session.save()
        students = User.objects.filter(enrollments__subject=session.subject, role=User.Role.STUDENT).distinct()
        with transaction.atomic():
            for student in students:
                AttendanceRecord.objects.get_or_create(session=session, student=student, defaults={"status": "ABSENT", "marked_by": request.user})
        messages.success(request, "Class session created. Review and update the attendance register.")
        return redirect("session_detail", session_id=session.pk)
    return render(request, "attendance/mark.html", {"form": form})


@login_required
def session_detail(request, session_id):
    session = get_object_or_404(ClassSession.objects.select_related("subject", "faculty"), pk=session_id)
    if not faculty_can_teach(request.user, session.subject):
        return HttpResponseForbidden()
    if request.user.role not in [User.Role.FACULTY, User.Role.ADMIN] and not request.user.is_superuser:
        return HttpResponseForbidden()
    FormSet = modelformset_factory(AttendanceRecord, fields=("status",), extra=0)
    qs = session.records.select_related("student")
    formset = FormSet(request.POST or None, queryset=qs)
    if request.method == "POST" and formset.is_valid():
        instances = formset.save(commit=False)
        for record in instances:
            record.marked_by = request.user
            record.save()
        messages.success(request, "Attendance updated.")
        return redirect("session_detail", session_id=session.pk)
    concerns = AttendanceConcern.objects.filter(record__session=session).select_related("student", "record__session")
    return render(request, "attendance/session_detail.html", {"session": session, "formset": formset, "concerns": concerns})


@login_required
def raise_attendance_concern(request, record_id):
    record = get_object_or_404(AttendanceRecord.objects.select_related("session__subject"), pk=record_id, student=request.user)
    if request.user.role != User.Role.STUDENT:
        return HttpResponseForbidden()
    if record.status != AttendanceRecord.Status.ABSENT:
        messages.info(request, "You can raise a concern only for an absent attendance entry.")
        return redirect("dashboard")
    if record.concerns.filter(status__in=[AttendanceConcern.Status.OPEN, AttendanceConcern.Status.REVIEWING]).exists():
        messages.info(request, "You already have an open concern for this attendance entry.")
        return redirect("dashboard")
    form = AttendanceConcernForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        concern = form.save(commit=False)
        concern.record = record
        concern.student = request.user
        concern.save()
        messages.success(request, "Your attendance concern has been sent to the faculty member.")
        return redirect("dashboard")
    return render(request, "attendance/raise_concern.html", {"form": form, "record": record})


@login_required
def review_concern(request, concern_id):
    concern = get_object_or_404(AttendanceConcern.objects.select_related("record__session__subject", "student"), pk=concern_id)
    subject = concern.record.session.subject
    if not faculty_can_teach(request.user, subject):
        return HttpResponseForbidden()
    if request.user.role not in [User.Role.FACULTY, User.Role.ADMIN] and not request.user.is_superuser:
        return HttpResponseForbidden()
    form = ConcernReviewForm(request.POST or None, instance=concern)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Concern review saved.")
        return redirect("session_detail", session_id=concern.record.session_id)
    return render(request, "attendance/review_concern.html", {"form": form, "concern": concern})
