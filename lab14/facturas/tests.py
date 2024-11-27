from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Factura
from clientes.models import Cliente
from proveedores.models import Proveedor

class FacturaTests(APITestCase):
    def setUp(self):
        # Crear cliente y proveedor
        self.cliente = Cliente.objects.create(nombre='Cliente 1', correo='cliente10example.com')
        self.proveedor = Proveedor.objects.create(nombre='Proveedor 1', correo='proveedor1@example.com')
        # Crear factura
        self.factura = Factura.objects.create(
            numero_factura='FAC001',
            cliente=self.cliente,
            fecha_emision='2024-01-01',
            fecha_vencimiento='2024-01-15',
            monto_total=1000.00,
            estado='Pendiente',
            tipo='Cobrar'
        )
        self.factura_proveedor = Factura.objects.create(
            numero_factura='FAC002',
            proveedor=self.proveedor,
            fecha_emision='2024-01-05',
            fecha_vencimiento='2024-01-20',
            monto_total=1500.00,
            estado='Pendiente',
            tipo='Pagar'
        )

    def test_listar_facturas(self):
        url = reverse('lista_crear_facturas')
        response = self.client.get(url, HTTP_X_USER_ROLE='Administrador')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_crear_factura(self):
        url = reverse('lista_crear_facturas')
        data = {
            'numero_factura': 'FAC003',
            'cliente': self.cliente.id,
            'fecha_emision': '2024-02-01',
            'fecha_vencimiento': '2024-02-15',
            'monto_total': 2000.00,
            'estado': 'Pendiente',
            'tipo': 'Cobrar'
        }
        response = self.client.post(url, data, HTTP_X_USER_ROLE='Administrador')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_editar_factura_administrador(self):
        url = reverse('editar_factura', kwargs={'pk': self.factura.pk})
        data = {
            'monto_total': 1200.00
        }
        response = self.client.put(url, data, HTTP_X_USER_ROLE='Administrador')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['monto_total'], '1200.00')

    def test_editar_factura_gerente_estado(self):
        url = reverse('editar_factura', kwargs={'pk': self.factura.pk})
        data = {
            'estado': 'Pagada'
        }
        response = self.client.put(url, data, HTTP_X_USER_ROLE='Gerente')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['estado'], 'Pagada')

    def test_permiso_denegado_editar_factura(self):
        url = reverse('editar_factura', kwargs={'pk': self.factura.pk})
        data = {
            'estado': 'Pagada'
        }
        response = self.client.put(url, data, HTTP_X_USER_ROLE='Contador')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
