from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from rest_framework.authtoken.models import Token
from datetime import timedelta

class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    high_score = models.IntegerField(default=0)
    uid = models.CharField(default = "", max_length = 200)

    def __str__(self):
        return f"{self.user.username} - {self.high_score}"

class ExpiringToken(Token):
    def has_expired(self):
        """Check if the token has expired (24 hours in this case)."""
        now = timezone.now()
        expiration_time = self.created + timedelta(hours=24)  # Token valid for 24 hours
        return now > expiration_time