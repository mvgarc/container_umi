from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class Role(models.TextChoices):
    ADMIN = 'admin', _('Administrador')
    MANAGER = 'manager', _('Gerente')
    OPERATOR = 'operator', _('Operador')
    VIEWER = 'viewer', _('Solo lectura')

class CustomUser(AbstractUser):
    role = models.CharField(
        _("Rol de usuario"),
        max_length=20,
        choices=Role.choices,
        default=Role.VIEWER
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    class Meta:
        verbose_name = _("Usuario")
        verbose_name_plural = _("Usuarios")