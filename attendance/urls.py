from django.urls import path
from . import views

urlpatterns = [
    path("mark/", views.mark_attendance, name="mark_attendance"),
    path("session/<int:session_id>/", views.session_detail, name="session_detail"),
    path("record/<int:record_id>/concern/", views.raise_attendance_concern, name="raise_attendance_concern"),
    path("concern/<int:concern_id>/review/", views.review_concern, name="review_concern"),
]
