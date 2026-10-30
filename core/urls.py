from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="core/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("farms/", views.farms, name="farms"),
    path("soil/", views.soil, name="soil"),
    path("recommendations/", views.crop_recommendation, name="recommend"),
    path("weather/", views.weather, name="weather"),
    path("disease/", views.disease, name="disease"),
    path("market/", views.market, name="market"),
    path("control-room/", views.admin_dashboard, name="admin_dashboard"),
    path("control-room/farmers/", views.admin_farmers, name="admin_farmers"),
    path("control-room/reports/", views.admin_reports, name="admin_reports"),
    path("control-room/reports/", views.admin_reports, name="admin_reports")
]
