from functools import wraps
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

def role_required(allowed_roles=None):
    """
    Decorador para restringir el acceso según el rol del usuario.
    Ejemplo de uso:
    @role_required(['admin', 'manager'])
    def vista(...):
        ...
    """
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if user.is_superuser or user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("No tienes permiso para acceder a esta vista.")
        return _wrapped_view
    return decorator
