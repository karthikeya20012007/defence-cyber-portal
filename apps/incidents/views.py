import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Incident


@login_required
def submit_incident(request):
    if request.method == "POST":
        description = request.POST.get("description")

        response = requests.post(
            "http://127.0.0.1:8001/predict",
            json={"description": description}
        )

        data = response.json()

        Incident.objects.create(
            user=request.user,
            description=description,
            threat_type=data["threat_type"],
            risk_score=data["risk_score"],
            status=data["status"]
        )

        return redirect("dashboard")

    return render(request, "submit_incident.html")


@login_required
def dashboard(request):
    incidents = Incident.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "dashboard.html", {"incidents": incidents})