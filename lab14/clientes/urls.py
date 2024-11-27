from django.urls import path
from .views import ListaClientesView, DetalleClienteView

# Configuración de las URLs para Cliente
urlpatterns = [
    path('lista/', ListaClientesView.as_view(), name='lista_clientes'),
    path('<int:pk>/', DetalleClienteView.as_view(), name='detalle_cliente'),
]