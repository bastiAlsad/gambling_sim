from rest_framework import serializers
from django.contrib.auth.models import User
from .models import PlayerProfile
from uuid import uuid4

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        uid = str(uuid4())
        while PlayerProfile.objects.filter(uid=uid).exists():
            uid = str(uuid4())
        PlayerProfile.objects.create(user=user, uid=uid)
        return user


class PlayerProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = PlayerProfile
        fields = ['user', 'high_score']
