from rest_framework.decorators import api_view, authentication_classes, permission_classes, renderer_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from django.contrib.auth.models import User
from .models import ExpiringToken, PlayerProfile
from .serializers import UserSerializer
from uuid import uuid4
from . import models

# Registrierung eines neuen Benutzers und Erstellen eines Tokens
@api_view(["POST"])
@renderer_classes([JSONRenderer])  # Erzwinge JSON-Antwort
def register_user(request):
    print("register funktion called")
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        uid = str(uuid4())
        while models.PlayerProfile.objects.filter(uid=uid).exists():
              uid = str(uuid4())
        user = serializer.save()  
        player_object = models.PlayerProfile.objects.get(user=user)  # Hole das PlayerProfile-Objekt
        player_object.uid = uid  # Setze die UID
        player_object.save()  # Speichere das Objekt

        token, created = ExpiringToken.objects.get_or_create(user=user)
        print(f"token: {token.key}")
        print(f"uid: {uid}")
        return Response({
            'token': token.key,
            'uid': uid,
            'message': 'User registered successfully!'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Benutzer-Login und Token erstellen
@api_view(["POST"])
@renderer_classes([JSONRenderer])  # Erzwinge JSON-Antwort
def login_user(request):
    print("login funktion called")
    username = request.data.get('username')
    password = request.data.get('password')
    user = User.objects.filter(username=username).first()
    if user and user.check_password(password):
        # Prüfen, ob ein Token bereits existiert und abgelaufen ist
        token, created = ExpiringToken.objects.get_or_create(user=user)
        if not created:
            if token.has_expired():
                token.delete()  # Lösche den abgelaufenen Token
                token = ExpiringToken.objects.create(user=user)  # Erstelle einen neuen Token
        return Response({
            'token': token.key,
            'uid': models.PlayerProfile.objects.get(user=user).uid,
            'message': 'Login successful!'
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@renderer_classes([JSONRenderer])  # Erzwinge JSON-Antwort
def get_ranking(request):
    print("ranking funktion called")
    players = PlayerProfile.objects.order_by('-coins')
    player_data = [{'username': player.user.username, 'coins': player.coins} for player in players]
    print(f"player_data: {player_data}")
    return Response(player_data, status=status.HTTP_200_OK)

# Update Coins Method
@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@renderer_classes([JSONRenderer])  # Erzwinge JSON-Antwort
def update_coins(request):
    coins_amount = request.data.get('coins_amount', None)
    uid = request.data.get('uid', None)
    if coins_amount is None:
        return Response({"error": "No score provided"}, status=status.HTTP_400_BAD_REQUEST)

    player_profile = models.PlayerProfile.objects.get(uid=uid)
    player_profile.coins = coins_amount
    player_profile.save()
    return Response({"message": "Coins score updated"}, status=status.HTTP_200_OK)
    