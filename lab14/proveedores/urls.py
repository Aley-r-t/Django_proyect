from django.urls import path
from .views import ListaProveedoresView, DetalleProveedorView

urlpatterns = [
    path('proveedores/', ListaProveedoresView.as_view(), name='lista_proveedores'),
    path('proveedores/<int:pk>/', DetalleProveedorView.as_view(), name='detalle_proveedor'),
]
