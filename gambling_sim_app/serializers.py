from rest_framework import serializers
from django.contrib.auth.models import User
from .models import PlayerProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        PlayerProfile.objects.create(user=user)  
        return user


class PlayerProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = PlayerProfile
        fields = ['user', 'coins']
