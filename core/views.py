from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import render
from accounts.models import User
from academics.models import AcademicBatch, Course, Department, Enrollment, FacultySubjectAssignment, StudentProfile, Subject, TimetableEntry
from attendance.models import AttendanceConcern, AttendanceRecord, ClassSession


def home(request):
    return render(request, "core/home.html")


@login_required
def dashboard(request):
    user = request.user
    if user.role == User.Role.STUDENT and not user.is_superuser:
        records = AttendanceRecord.objects.filter(student=user, session__status="COMPLETED").select_related("session__subject__course__department", "session__faculty").prefetch_related("session__subject__faculty_assignments__faculty")
        total = records.count()
        present = records.filter(status=AttendanceRecord.Status.PRESENT).count()
        concerns = AttendanceConcern.objects.filter(student=user).select_related("record__session__subject")
        profile = StudentProfile.objects.filter(student=user).select_related("batch__course__department").first()
        semester_data = []
        semester_values = sorted(set(records.values_list("session__subject__semester", flat=True)), reverse=True)
        if profile:
            semester_values = sorted(set(semester_values) | set(range(1, profile.current_semester + 1)), reverse=True)
        for semester in semester_values:
            semester_records = records.filter(session__subject__semester=semester)
            count = semester_records.count()
            attended = semester_records.filter(status=AttendanceRecord.Status.PRESENT).count()
            semester_data.append({
                "number": semester, "total": count, "present": attended,
                "absent": semester_records.filter(status=AttendanceRecord.Status.ABSENT).count(),
                "percentage": round(100 * attended / count, 1) if count else 0,
                "subjects": Enrollment.objects.filter(student=user, subject__semester=semester).select_related("subject", "subject__course"),
            })
        current_semester = profile.current_semester if profile else (semester_values[0] if semester_values else 1)
        current_subjects = Enrollment.objects.filter(student=user, subject__semester=current_semester).select_related("subject", "subject__course").prefetch_related("subject__faculty_assignments__faculty").annotate(total_classes=Count("subject__sessions__records", filter=Q(subject__sessions__status="COMPLETED", subject__sessions__records__student=user)), present_classes=Count("subject__sessions__records", filter=Q(subject__sessions__status="COMPLETED", subject__sessions__records__student=user, subject__sessions__records__status="PRESENT")) )
        return render(request, "dashboards/student.html", {
            "total": total, "present": present,
            "absent": records.filter(status=AttendanceRecord.Status.ABSENT).count(),
            "late": records.filter(status=AttendanceRecord.Status.LATE).count(),
            "percentage": round(100 * present / total, 1) if total else 0,
            "recent": records, "concerns": concerns[:20],
            "open_concerns": concerns.filter(status__in=["OPEN", "REVIEWING"]).count(),
            "profile": profile, "semester_data": semester_data,\n            "timetable": profile.batch.timetable_entries.select_related("subject", "faculty") if profile else [],
            "current_semester": current_semester, "current_subjects": current_subjects,
        })
    if user.role == User.Role.FACULTY and not user.is_superuser:
        assignments = FacultySubjectAssignment.objects.filter(faculty=user).select_related("subject__course__department")
        subjects = Subject.objects.filter(Q(faculty_assignments__faculty=user) | Q(faculty=user)).distinct().select_related("course__department").annotate(enrolled_students=Count("enrollments", distinct=True))
        sessions = ClassSession.objects.filter(Q(faculty=user) | Q(subject__faculty=user) | Q(subject__faculty_assignments__faculty=user)).distinct().select_related("subject", "subject__course")[:20]
        concerns = AttendanceConcern.objects.filter(
            Q(record__session__faculty=user) | Q(record__session__subject__faculty=user) | Q(record__session__subject__faculty_assignments__faculty=user)
        ).select_related("student", "record__session__subject").distinct()
        return render(request, "dashboards/faculty.html", {
            "subjects": subjects, "assignments": assignments, "sessions": sessions,\n            "timetable": TimetableEntry.objects.filter(faculty=user).select_related("subject", "batch__course"),
            "session_count": ClassSession.objects.filter(Q(faculty=user) | Q(subject__faculty=user) | Q(subject__faculty_assignments__faculty=user)).distinct().count(),
            "pending_concerns": concerns.filter(status__in=["OPEN", "REVIEWING"])[:20],
            "pending_count": concerns.filter(status__in=["OPEN", "REVIEWING"]).count(),
        })
    return render(request, "dashboards/admin.html", {
        "students": User.objects.filter(role=User.Role.STUDENT).count(),
        "faculty": User.objects.filter(role=User.Role.FACULTY).count(),
        "subjects": Subject.objects.count(),
        "departments": Department.objects.count(),
        "programmes": Course.objects.count(),
        "batches": AcademicBatch.objects.count(),
        "sessions": ClassSession.objects.count(),
        "concerns": AttendanceConcern.objects.filter(status__in=["OPEN", "REVIEWING"]).count(),
    })
