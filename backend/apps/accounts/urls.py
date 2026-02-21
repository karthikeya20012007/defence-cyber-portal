from . import views
from django.urls import path

urlpatterns = [
    path("", views.landing_page, name="landing"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),

    path("dashboard/reporter/", views.reporter_dashboard, name="reporter_dashboard"),
    path("dashboard/admin/", views.admin_dashboard, name="admin_dashboard"),

    path("report/", views.report_incident, name="report_incident"),
]