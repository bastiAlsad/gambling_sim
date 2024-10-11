# views.py
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import ExpiringToken, PlayerProfile
from .serializers import UserSerializer
from uuid import uuid4
from . import models


# Registrierung eines neuen Benutzers und Erstellen eines Tokens
@api_view(["POST"])
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
        print(f"uid: {uid.key}")
        return Response({
            'token': token.key,
            'uid': uid,
            'message': 'User registered successfully!'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Benutzer-Login und Token erstellen
@api_view(["POST"])
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
            'uid': models.PlayerProfile.objects.get(user = user).uid,
            'message': 'Login successful!'
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)

# Beispiel einer geschützten Funktion, um das Ranking zu erhalten
@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_ranking(request):
    print("ranking funktion called")
    players = PlayerProfile.objects.order_by('-high_score')
    player_data = [{'username': player.user.username, 'high_score': player.high_score} for player in players]
    print(f"player_data: {player_data}")
    return Response(player_data, status=status.HTTP_200_OK)

# Highscore-Update für eingeloggte Benutzer
@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_highscore(request):
    print("update_highscore funktion called")
    current_score = request.data.get('current_score', None)
    uid = request.data.get('uid', None)
    if current_score is None:
        return Response({"error": "No score provided"}, status=status.HTTP_400_BAD_REQUEST)

    player_profile =  models.PlayerProfile.objects.get(uid = uid)
    if int(current_score) > player_profile.high_score:
        player_profile.high_score = current_score
        player_profile.save()
        return Response({"message": "High score updated"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "No update, score is not higher"}, status=status.HTTP_200_OK)
