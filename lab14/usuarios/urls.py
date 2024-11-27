
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import ListaUsuariosView, CustomTokenObtainPairView

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('lista/', ListaUsuariosView.as_view(), name='lista_usuarios'),
]