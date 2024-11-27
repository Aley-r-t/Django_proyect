from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Usuario
from rest_framework import status
from .serializers import UsuarioSerializer

from django.contrib.auth.hashers import make_password
from .roles import verificar_rol_usuario


# Vista para listar usuarios, ejemplo del uso del permiso personalizado
class ListaUsuariosView(APIView):
    def get(self, request):
        # Verificar si el usuario tiene un rol permitido
        if not verificar_rol_usuario(request, ["Administrador", "Gerente"]):
            return Response({'detail': 'Permiso denegado'}, status=403)

        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)
    
class DetalleUsuarioView(APIView):
    def get(self, request, pk):
        # Verificar si el usuario tiene un rol permitido
        if not verificar_rol_usuario(request, ["Administrador", "Gerente"]):
            return Response({'detail': 'Permiso denegado'}, status=403)
        
        try:
            usuario = Usuario.objects.get(pk=pk)
        except Usuario.DoesNotExist:
            return Response({'detail': 'Usuario no encontrado'}, status=404)
        
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)
    
class CrearUsuarioView(APIView):
    def post(self, request):
        # Verificar si el usuario tiene un rol permitido
        if not verificar_rol_usuario(request, ["Administrador"]):
            return Response({'detail': 'Permiso denegado'}, status=403)
        
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(password=make_password(request.data.get('password')))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EliminarUsuarioView(APIView):
    def delete(self, request, pk):
        # Verificar si el usuario tiene un rol permitido
        if not verificar_rol_usuario(request, ["Administrador"]):
            return Response({'detail': 'Permiso denegado'}, status=403)
        
        try:
            usuario = Usuario.objects.get(pk=pk)
        except Usuario.DoesNotExist:
            return Response({'detail': 'Usuario no encontrado'}, status=404)
        
        usuario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# Generar tokens JWT para un usuario
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        usuario = Usuario.objects.filter(correo=request.data.get('correo')).first()
        if usuario and usuario.check_password(request.data.get('password')):
            refresh = RefreshToken.for_user(usuario)
            response = Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'usuario': UsuarioSerializer(usuario).data
            })
            response['X-User-Role'] = usuario.rol  # Agregar el rol del usuario al encabezado
            return response
        return Response({'error': 'Credenciales incorrectas'}, status=400)

usuario = Usuario(
    nombre="Alex",
    correo="alex@gmail.com",
    password=make_password("admin123"),
    rol="Administrador",
    is_active=True,
    is_admin=True
)