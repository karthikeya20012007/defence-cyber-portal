from django.urls import path
from .views import (
    register_view,
    login_view,
    logout_view,
    dashboard_view,
    operational_dashboard,
    reporter_dashboard,
)

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    path("dashboard/", dashboard_view, name="dashboard"),
    path("dashboard/operational/", operational_dashboard, name="operational_dashboard"),
    path("dashboard/reporter/", reporter_dashboard, name="reporter_dashboard"),
]