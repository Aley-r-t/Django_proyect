from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Usuario

class TieneRolPermitido(BasePermission):
    def __init__(self, roles_permitidos):
        self.roles_permitidos = roles_permitidos

    def has_permission(self, request, view):
        # Comprobar si el usuario está autenticado usando JWT
        jwt_authenticator = JWTAuthentication()
        try:
            user, validated_token = jwt_authenticator.authenticate(request)
            if user is None:
                return False
        except Exception:
            return False

        # Comprobar si el usuario tiene un rol permitido
        usuario = Usuario.objects.filter(correo=user.email).first()
        if usuario and usuario.rol in self.roles_permitidos:
            return True
        
        return False