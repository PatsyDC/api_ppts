from django.conf import settings
from django.urls import path, include
from .views import *

urlpatterns = [
    path('publicaciones/', PresentationListCreateView.as_view(), name ='public'),
    path('presentaciones/', PresentacionesPorFecha.as_view(), name='presentaciones-por-fecha'),
    path('publicaciones/<int:pk>', PresentationRetrieveUpdateDestroyView.as_view(), name = 'publicid'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user-list'),
]