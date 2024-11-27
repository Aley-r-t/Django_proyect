from django.urls import path
from .views import ListaCrearFacturasView, EditarFacturaView

# Configuración de las URLs para Facturas
urlpatterns = [
    path('facturas/', ListaCrearFacturasView.as_view(), name='lista_crear_facturas'),
    path('facturas/<int:pk>/', EditarFacturaView.as_view(), name='editar_factura'),
]