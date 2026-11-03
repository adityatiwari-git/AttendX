from django.urls import path
from . import views
urlpatterns = [path("mark/",views.mark_attendance,name="mark_attendance"),path("session/<int:session_id>/",views.session_detail,name="session_detail")]
