from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from rest_framework.authtoken.models import Token
from datetime import timedelta

class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coins = models.IntegerField(default=10000)
    uid = models.CharField(default="", max_length=200, unique=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - Coins: {self.coins}"

class ExpiringToken(Token):
    def has_expired(self):
        """Check if the token has expired (24 hours in this case)."""
        now = timezone.now()
        expiration_time = self.created + timedelta(hours=24)
        return now > expiration_time
    
    class Meta:
        # Stelle sicher, dass die Tabelle korrekt benannt wird
        db_table = 'gambling_sim_app_expiringtoken'