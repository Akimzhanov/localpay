from rest_framework import serializers


from .models import Pays
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'


    def create(self, validated_data):
        a = validated_data['is_active']
        a = True
        validated_data['is_active'] = a
        b = validated_data['access']
        b = True
        validated_data['access'] = b
        user = User.objects.create_user(**validated_data)
        return user

