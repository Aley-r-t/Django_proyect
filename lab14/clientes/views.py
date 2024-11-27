from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cliente
from .serializers import ClienteSerializer
from usuarios.roles import verificar_rol_usuario

# Vista para listar clientes
class ListaClientesView(APIView):
    def get(self, request):
        # Verificar si el usuario tiene un rol permitido
        if not verificar_rol_usuario(request, ["Administrador", "Gerente"]):
            return Response({'detail': 'Permiso denegado'}, status=403)

        clientes = Cliente.objects.all()
        serializer = ClienteSerializer(clientes, many=True)
        return Response(serializer.data)

# Vista para ver detalles de un cliente específico
class DetalleClienteView(APIView):
    def get(self, request, pk):
        # Verificar si el usuario tiene un rol permitido
        if not verificar_rol_usuario(request, ["Administrador", "Gerente"]):
            return Response({'detail': 'Permiso denegado'}, status=403)
        
        try:
            cliente = Cliente.objects.get(pk=pk)
        except Cliente.DoesNotExist:
            return Response({'detail': 'Cliente no encontrado'}, status=404)
        
        serializer = ClienteSerializer(cliente)
        return Response(serializer.data)