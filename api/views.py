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
from django.db.models import Q
from datetime import datetime

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

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": serializer.data,
                "message": "Usuario creado exitosamente"
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

########### PRESENTACIONES #################
class PresentationListCreateView(generics.ListCreateAPIView):
    serializer_class = PresentationSerializer

    def get_queryset(self):
        queryset = Presentation.objects.all()
        fecha_str = self.request.query_params.get('fecha', None)
        
        if fecha_str:
            try:
                # Ya que usamos DateField, podemos filtrar directamente
                queryset = queryset.filter(fecha=fecha_str)
                print(f"Fecha buscada: {fecha_str}")
                print(f"Registros encontrados: {queryset.count()}")
                # Debug: imprimir todas las fechas disponibles
                todas_fechas = Presentation.objects.values_list('fecha', flat=True).distinct()
                print(f"Fechas disponibles en la BD: {list(todas_fechas)}")
            except Exception as e:
                print(f"Error al filtrar: {e}")
                return Presentation.objects.none()
        
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        # Debug: imprimir información útil
        print(f"Query params recibidos: {request.query_params}")
        print(f"Cantidad de registros encontrados: {queryset.count()}")
        print(f"Datos serializados: {serializer.data}")
        
        return Response(serializer.data)

class PresentationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Presentation.objects.all()
    serializer_class = PresentationSerializer
