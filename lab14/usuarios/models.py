from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.

class Usuario(AbstractBaseUser):
    ROLES = [
        ("Administrador", "Administrador"),
        ("Contador", "Contador"),
        ("Gerente", "Gerente"),
    ]

    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    rol = models.CharField(max_length=50, choices=ROLES)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        return self.nombre

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
  

