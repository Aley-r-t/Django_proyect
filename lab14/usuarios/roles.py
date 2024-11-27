def verificar_rol_usuario(request, roles_permitidos):
    # Comprobar si el rol del usuario está en los headers y tiene un rol permitido
    user_role = request.headers.get('X-User-Role')
    if user_role and user_role in roles_permitidos:
        return True
    return False