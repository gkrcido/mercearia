from rest_framework import serializers
from .models import Cereal, Laticinio, Fruta, Legume, Verdura, CustomUser, BaseUserManager, AbstractBaseUser
from rest_framework import serializers
from django.contrib.auth.models import User

class CerealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cereal
        fields = '__all__'

class LaticinioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laticinio
        fields = '__all__'

class FrutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fruta
        fields = '__all__'

class LegumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Legume
        fields = '__all__'

class VerduraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verdura
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']  # Adicione os campos necessários

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user