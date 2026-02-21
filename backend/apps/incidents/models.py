from django.db import models
from django.conf import settings


class Incident(models.Model):

    SEVERITY_CHOICES = (
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
        ("CRITICAL", "Critical"),
    )

    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("UNDER_REVIEW", "Under Review"),
        ("RESOLVED", "Resolved"),
        ("REJECTED", "Rejected"),
    )

    # Basic Info
    title = models.CharField(max_length=255)
    description = models.TextField()

    # Classification
    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        default="LOW"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    # AI / ML
    risk_score = models.FloatField(default=0.0)  # 0–100

    # Evidence
    evidence_file = models.FileField(
        upload_to="incident_evidence/",
        null=True,
        blank=True
    )

    # Metadata
    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="incidents"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.title}"