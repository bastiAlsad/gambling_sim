# authentication.py (optional)
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import ExpiringToken

class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = ExpiringToken.objects.get(key=key)
        except ExpiringToken.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        if token.has_expired():
            token.delete()
            raise AuthenticationFailed('Token has expired')

        return (token.user, token)
