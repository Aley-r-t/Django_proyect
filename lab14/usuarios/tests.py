from django.test import TestCase

# Create your tests here.

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Usuario
from django.contrib.auth.hashers import make_password

class UsuarioTests(APITestCase):

    def setUp(self):
        # Crear un usuario administrador para las pruebas
        self.admin_user = Usuario.objects.create(
            nombre="Admin User",
            correo="admin@test.com",
            password=make_password("admin123"),
            rol="Administrador",
            is_admin=True
        )
        # Crear un usuario gerente para las pruebas
        self.manager_user = Usuario.objects.create(
            nombre="Manager User",
            correo="manager@test.com",
            password=make_password("manager123"),
            rol="Gerente"
        )
        # Crear un usuario para autenticación
        self.login_url = reverse('token_obtain_pair')
        self.client.post(self.login_url, {'correo': 'admin@test.com', 'password': 'admin123'})

    def test_listar_usuarios(self):
        url = reverse('lista_usuarios')
        response = self.client.get(url, HTTP_X_USER_ROLE='Administrador')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ver_detalle_usuario(self):
        url = reverse('detalle_usuario', kwargs={'pk': self.manager_user.pk})
        response = self.client.get(url, HTTP_X_USER_ROLE='Gerente')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_crear_usuario(self):
        url = reverse('crear_usuario')
        data = {
            'nombre': 'New User',
            'correo': 'newuser@test.com',
            'password': 'newuser123',
            'rol': 'Contador'
        }
        response = self.client.post(url, data, HTTP_X_USER_ROLE='Administrador')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_eliminar_usuario(self):
        url = reverse('eliminar_usuario', kwargs={'pk': self.manager_user.pk})
        response = self.client.delete(url, HTTP_X_USER_ROLE='Administrador')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
