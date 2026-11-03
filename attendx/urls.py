from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from accounts.forms import RoleAuthenticationForm
from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html", authentication_form=RoleAuthenticationForm), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("accounts/", include("accounts.urls")),
    path("attendance/", include("attendance.urls")),
]
