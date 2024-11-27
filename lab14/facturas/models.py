from django.db import models
from django.utils import timezone
from clientes.models import Cliente
from proveedores.models import Proveedor
# Create your models here.

class Factura(models.Model):
    ESTADO_OPCIONES = [
        ('Pendiente', 'Pendiente'),
        ('Pagada', 'Pagada'),
        ('Vencida', 'Vencida'),
    ]

    TIPO_OPCIONES = [
        ('Cobrar', 'Cobrar'),
        ('Pagar', 'Pagar'),
    ]

    numero_factura = models.CharField(max_length=50, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, related_name="facturas")
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True, related_name="facturas")
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField()
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_OPCIONES, default='Pendiente')
    tipo = models.CharField(max_length=10, choices=TIPO_OPCIONES)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def actualizar_estado(self):
        if self.fecha_vencimiento < timezone.now().date() and self.estado == 'Pendiente':
            self.estado = 'Vencida'
            self.save()

    def __str__(self):
        return f"Factura {self.numero_factura} - {self.estado}"