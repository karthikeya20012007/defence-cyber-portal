import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import IncidentForm


@login_required
def submit_incident(request):

    if request.method == "POST":
        form = IncidentForm(request.POST, request.FILES)

        if form.is_valid():
            incident = form.save(commit=False)
            incident.reported_by = request.user

            try:
                # ✅ Send correct JSON key
                response = requests.post(
                    "http://127.0.0.1:8001/predict",
                    json={"description": incident.description},
                    timeout=5
                )

                print("FastAPI status:", response.status_code)

                if response.status_code == 200:
                    data = response.json()
                    print("FastAPI response:", data)

                    # ✅ Map FastAPI fields to Django model
                    incident.risk_score = data.get("risk_score", 0)
                    incident.severity = data.get("status", "LOW")  # FastAPI returns 'status'
                    incident.status = "UNDER_REVIEW"

                else:
                    incident.status = "PENDING"

            except Exception as e:
                print("FastAPI connection error:", e)
                incident.status = "PENDING"

            incident.save()

            return redirect("reporter_dashboard")

        else:
            print("FORM ERRORS:", form.errors)

    else:
        form = IncidentForm()

    return render(request, "incidents/report_incident.html", {"form": form})