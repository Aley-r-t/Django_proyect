from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Proveedor

class ProveedorTests(APITestCase):

    def setUp(self):
        # Crear proveedores iniciales
        Proveedor.objects.bulk_create([
            Proveedor(nombre='Proveedor 1', correo='proveedor1@example.com', telefono='123456789', direccion='Dirección A'),
            Proveedor(nombre='Proveedor 2', correo='proveedor2@example.com', telefono='987654321', direccion='Dirección B'),
            Proveedor(nombre='Proveedor 3', correo='proveedor3@example.com', telefono='555555555', direccion='Dirección C'),
        ])

    def test_listar_proveedores(self):
        url = reverse('lista_proveedores')
        response = self.client.get(url, HTTP_X_USER_ROLE='Administrador')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_ver_detalle_proveedor(self):
        proveedor = Proveedor.objects.first()
        url = reverse('detalle_proveedor', kwargs={'pk': proveedor.pk})
        response = self.client.get(url, HTTP_X_USER_ROLE='Gerente')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], proveedor.nombre)

    def test_permiso_denegado_listar_proveedores(self):
        url = reverse('lista_proveedores')
        response = self.client.get(url, HTTP_X_USER_ROLE='Contador')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_proveedor_no_encontrado(self):
        url = reverse('detalle_proveedor', kwargs={'pk': 999})
        response = self.client.get(url, HTTP_X_USER_ROLE='Administrador')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
