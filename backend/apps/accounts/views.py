from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm
from apps.incidents.models import Incident
from apps.incidents.forms import IncidentForm


# ======================
# LANDING PAGE
# ======================

def landing_page(request):
    return render(request, "landing.html")


# ======================
# REGISTER
# ======================

def register_view(request):
    role = request.GET.get("role")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            if role:
                user.role = role

            if role == "admin":
                user.is_staff = True

            user.save()
            return redirect("login")

    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


# ======================
# LOGIN
# ======================

def login_view(request):

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = form.cleaned_data["user"]
            login(request, user)

            # Redirect based on role
            if user.role == "admin":
                return redirect("admin_dashboard")
            else:
                return redirect("reporter_dashboard")

    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


# ======================
# LOGOUT
# ======================

@login_required
def logout_view(request):
    logout(request)
    return redirect("landing")


# ======================
# REPORT INCIDENT (SAVE LOGIC)
# ======================

@login_required
def report_incident(request):

    if request.method == "POST":
        form = IncidentForm(request.POST, request.FILES)

        if form.is_valid():
            incident = form.save(commit=False)
            incident.reported_by = request.user
            incident.save()

            return redirect("reporter_dashboard")

    else:
        form = IncidentForm()

    return render(request, "incidents/report_incident.html", {"form": form})


# ======================
# REPORTER DASHBOARD
# ======================

@login_required
def reporter_dashboard(request):

    incidents = Incident.objects.filter(
        reported_by=request.user
    ).order_by("-created_at")

    context = {
        "incidents": incidents,
        "total_reports": incidents.count(),
        "high_risk": incidents.filter(severity__in=["HIGH", "CRITICAL"]).count(),
        "resolved_count": incidents.filter(status="RESOLVED").count(),
    }

    return render(request, "accounts/reporter_dashboard.html", context)


# ======================
# ADMIN DASHBOARD
# ======================

@login_required
def admin_dashboard(request):

    incidents = Incident.objects.all().order_by("-created_at")

    context = {
        "incidents": incidents,
        "total_incidents": incidents.count(),
        "critical_count": incidents.filter(severity="CRITICAL").count(),
        "resolved_count": incidents.filter(status="RESOLVED").count(),
    }

    return render(request, "accounts/operational_dashboard.html", context)