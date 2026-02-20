from django.db import models
from django.conf import settings


class Incident(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="incidents"
    )

    title = models.CharField(max_length=255)
    description = models.TextField()

    threat_type = models.CharField(max_length=100)

    risk_score = models.FloatField(default=0.0)
    priority_score = models.FloatField(default=0.0)

    status = models.CharField(
        max_length=50,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title