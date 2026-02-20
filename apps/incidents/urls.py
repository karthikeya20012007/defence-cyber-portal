from django.urls import path
from .views import submit_incident, dashboard

urlpatterns = [
    path('submit/', submit_incident, name='submit_incident'),
    path('dashboard/', dashboard, name='dashboard'),
]