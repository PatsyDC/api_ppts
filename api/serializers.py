from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class PresentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presentation
        fields = ['id', 'user', 'description', 'image_before', 'image_after', 'fecha']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Asegurarnos de que la fecha se formatea correctamente
        representation['fecha'] = instance.fecha.strftime('%Y-%m-%d')
        return representation

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)  # Para confirmar la contraseña

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])  # Encripta la contraseña
        user.save()
        return user