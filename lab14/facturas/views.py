from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Factura
from .serializers import FacturaSerializer
from usuarios.roles import verificar_rol_usuario

# Create your views here.

class ListaCrearFacturasView(APIView):
    def get(self, request):
        # Verificar si el usuario tiene un rol permitido
        if not verificar_rol_usuario(request, ["Administrador", "Gerente", "Contador"]):
            return Response({'detail': 'Permiso denegado'}, status=403)

        facturas = Factura.objects.all()
        for factura in facturas:
            factura.actualizar_estado()
        serializer = FacturaSerializer(facturas, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Verificar si el usuario tiene un rol permitido
        if not verificar_rol_usuario(request, ["Administrador", "Gerente"]):
            return Response({'detail': 'Permiso denegado'}, status=403)
        
        serializer = FacturaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditarFacturaView(APIView):
    def put(self, request, pk):
        # Verificar si el usuario tiene un rol permitido
        if not verificar_rol_usuario(request, ["Administrador", "Gerente"]):
            return Response({'detail': 'Permiso denegado'}, status=403)
        
        try:
            factura = Factura.objects.get(pk=pk)
        except Factura.DoesNotExist:
            return Response({'detail': 'Factura no encontrada'}, status=404)
        
        if verificar_rol_usuario(request, ["Gerente"]):
            # Gerente solo puede actualizar el estado de la factura
            data = {'estado': request.data.get('estado')}
            serializer = FacturaSerializer(factura, data=data, partial=True)
        elif verificar_rol_usuario(request, ["Administrador"]):
            # Administrador puede actualizar cualquier campo
            serializer = FacturaSerializer(factura, data=request.data, partial=True)
        else:
            return Response({'detail': 'Permiso denegado'}, status=403)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)