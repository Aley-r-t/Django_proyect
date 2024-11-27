from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Usuario
from .serializers import UsuarioSerializer

from django.contrib.auth.hashers import make_password
from .roles import verificar_rol_usuario


# Vista para listar usuarios, ejemplo del uso del permiso personalizado
class ListaUsuariosView(APIView):
    def get(self, request):
        # Verificar si el usuario tiene un rol permitido
        if not verificar_rol_usuario(request, ["Gerente"]):
            return Response({'detail': 'Permiso denegado'}, status=403)

        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)

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