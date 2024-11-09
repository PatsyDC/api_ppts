from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import viewsets
from django.utils import timezone
from datetime import timedelta
from rest_framework import status #
from django.contrib.auth import authenticate #
from rest_framework_simplejwt.tokens import RefreshToken #
from .models import *
from .serializers import *

class CustomTokenObtainPairView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            try:
                user_token = UserToken.objects.get(user=user)
                if user_token.is_valid():
                    return Response({
                        'access': user_token.token,
                        'message': 'Token existente válido'
                    })
                else:
                    user_token.delete()
            except UserToken.DoesNotExist:
                pass
            
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            UserToken.objects.create(
                user=user,
                token=access_token,
                expires_at=timezone.now() + timedelta(minutes=60)  # Ajusta según tus necesidades
            )
            
            return Response({
                'access': access_token,
                'message': 'Nuevo token creado'
            })
        else:
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

########### PRESENTACIONES #################
class PresentationListCreateView(generics.ListCreateAPIView):
    queryset = Presentation.objects.all()
    serializer_class = PresentationSerializer

class PresentationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Presentation.objects.all()
    serializer_class = PresentationSerializer
