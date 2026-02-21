from django.urls import path
from . import views

app_name = "incidents"   # ✅ Namespace enabled

urlpatterns = [
    path("submit/", views.submit_incident, name="submit_incident"),
]