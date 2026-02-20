from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Incident(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    threat_type = models.CharField(max_length=100)
    risk_score = models.FloatField()
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.threat_type} - {self.risk_score}"