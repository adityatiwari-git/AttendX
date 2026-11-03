from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.models import User
from academics.models import Subject
from attendance.models import AttendanceConcern, AttendanceRecord, ClassSession


def home(request):
    return render(request, "core/home.html")


@login_required
def dashboard(request):
    user = request.user
    if user.role == User.Role.STUDENT and not user.is_superuser:
        records = AttendanceRecord.objects.filter(student=user, session__status="COMPLETED").select_related("session__subject").prefetch_related("concerns")
        total = records.count()
        present = records.filter(status=AttendanceRecord.Status.PRESENT).count()
        concerns = AttendanceConcern.objects.filter(student=user).select_related("record__session__subject")
        return render(request, "dashboards/student.html", {
            "total": total, "present": present,
            "absent": records.filter(status=AttendanceRecord.Status.ABSENT).count(),
            "late": records.filter(status=AttendanceRecord.Status.LATE).count(),
            "percentage": round(100 * present / total, 1) if total else 0,
            "recent": records[:30], "concerns": concerns[:10],
            "open_concerns": concerns.filter(status__in=["OPEN", "REVIEWING"]).count(),
        })
    if user.role == User.Role.FACULTY and not user.is_superuser:
        subjects = Subject.objects.filter(faculty=user)
        sessions = ClassSession.objects.filter(subject__faculty=user).select_related("subject")[:8]
        concerns = AttendanceConcern.objects.filter(record__session__subject__faculty=user).select_related("student", "record__session__subject")
        return render(request, "dashboards/faculty.html", {
            "subjects": subjects, "sessions": sessions,
            "session_count": ClassSession.objects.filter(subject__faculty=user).count(),
            "pending_concerns": concerns.filter(status__in=["OPEN", "REVIEWING"])[:10],
            "pending_count": concerns.filter(status__in=["OPEN", "REVIEWING"]).count(),
        })
    return render(request, "dashboards/admin.html", {
        "students": User.objects.filter(role=User.Role.STUDENT).count(),
        "faculty": User.objects.filter(role=User.Role.FACULTY).count(),
        "subjects": Subject.objects.count(),
        "sessions": ClassSession.objects.count(),
        "concerns": AttendanceConcern.objects.filter(status__in=["OPEN", "REVIEWING"]).count(),
    })
