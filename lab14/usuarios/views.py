from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Usuario
from .serializers import UsuarioSerializer
from .roles import TieneRolPermitido
from django.contrib.auth.hashers import make_password


# Vista para listar usuarios, ejemplo del uso del permiso personalizado
class ListaUsuariosView(APIView):
    permission_classes = [TieneRolPermitido(["Administrador", "Gerente"])]

    def get(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)

# Generar tokens JWT para un usuario
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        usuario = Usuario.objects.filter(correo=request.data.get('correo')).first()
        if usuario and usuario.check_password(request.data.get('password')):
            refresh = RefreshToken.for_user(usuario)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Credenciales incorrectas'}, status=400)

# Vista de inicio de sesión personalizada
class LoginView(APIView):
    def post(self, request):
        correo = request.data.get('correo')
        password = request.data.get('password')
        usuario = Usuario.objects.filter(correo=correo).first()
        if usuario and usuario.check_password(password):
            refresh = RefreshToken.for_user(usuario)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'usuario': UsuarioSerializer(usuario).data
            })
        return Response({'error': 'Credenciales incorrectas'}, status=400)
    

usuario = Usuario(
    nombre="Alex",
    correo="alex@gmail.com",
    password=make_password("admin123"),
    rol="Administrador",
    is_active=True,
    is_admin=True
)