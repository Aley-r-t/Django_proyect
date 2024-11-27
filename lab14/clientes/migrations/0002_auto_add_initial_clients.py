from django.db import migrations

# Función para crear registros iniciales de Clientes
def crear_clientes_iniciales(apps, schema_editor):
    Cliente = apps.get_model('clientes', 'Cliente')
    Cliente.objects.bulk_create([
        Cliente(nombre='Cliente 1', correo='cliente1@example.com', telefono='123456789', direccion='Dirección 1'),
        Cliente(nombre='Cliente 2', correo='cliente2@example.com', telefono='987654321', direccion='Dirección 2'),
        Cliente(nombre='Cliente 3', correo='cliente3@example.com', telefono='555555555', direccion='Dirección 3'),
    ])

# Archivo: migrations/0002_auto_add_initial_clients.py
class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0001_Cliente'),
    ]

    operations = [
        migrations.RunPython(crear_clientes_iniciales),
    ]