from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Proveedor
from .serializers import ProveedorSerializer
from usuarios.roles import verificar_rol_usuario



class ListaProveedoresView(APIView):
    def get(self, request):
        # Verificar si el usuario tiene un rol permitido
        if not verificar_rol_usuario(request, ["Administrador", "Gerente"]):
            return Response({'detail': 'Permiso denegado'}, status=403)

        proveedores = Proveedor.objects.all()
        serializer = ProveedorSerializer(proveedores, many=True)
        return Response(serializer.data)

# Vista para ver detalles de un proveedor específico
class DetalleProveedorView(APIView):
    def get(self, request, pk):
        # Verificar si el usuario tiene un rol permitido
        if not verificar_rol_usuario(request, ["Administrador", "Gerente"]):
            return Response({'detail': 'Permiso denegado'}, status=403)
        
        try:
            proveedor = Proveedor.objects.get(pk=pk)
        except Proveedor.DoesNotExist:
            return Response({'detail': 'Proveedor no encontrado'}, status=404)
        
        serializer = ProveedorSerializer(proveedor)
        return Response(serializer.data)