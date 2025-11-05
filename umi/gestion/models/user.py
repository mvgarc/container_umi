from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.TextChoices):
    ADMIN = 'admin', 'Administrador'
    MANAGER = 'manager', 'Gerente'
    OPERATOR = 'operator', 'Operador'
    VIEWER = 'viewer', 'Solo lectura'

class CustomUser(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.VIEWER
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
