from django.test import TestCase

# Create your tests here.


from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Cliente

class ClienteTests(APITestCase):

    def setUp(self):
        # Crear clientes iniciales
        Cliente.objects.bulk_create([
            Cliente(nombre='Cliente 1', correo='cliente7@example.com', telefono='123456789', direccion='Dirección 1'),
            Cliente(nombre='Cliente 2', correo='cliente8@example.com', telefono='987654321', direccion='Dirección 2'),
            Cliente(nombre='Cliente 3', correo='cliente9@example.com', telefono='555555555', direccion='Dirección 3'),
        ])

    def test_listar_clientes(self):
        url = reverse('lista_clientes')
        response = self.client.get(url, HTTP_X_USER_ROLE='Administrador')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)

    def test_ver_detalle_cliente(self):
        cliente = Cliente.objects.first()
        url = reverse('detalle_cliente', kwargs={'pk': cliente.pk})
        response = self.client.get(url, HTTP_X_USER_ROLE='Gerente')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], cliente.nombre)

    def test_permiso_denegado_listar_clientes(self):
        url = reverse('lista_clientes')
        response = self.client.get(url, HTTP_X_USER_ROLE='Contador')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cliente_no_encontrado(self):
        url = reverse('detalle_cliente', kwargs={'pk': 999})
        response = self.client.get(url, HTTP_X_USER_ROLE='Administrador')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)