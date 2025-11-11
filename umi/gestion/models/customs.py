from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomsAgent(models.Model):
    name = models.CharField(_("Nombre del Agente"), max_length=100)
    phone = models.CharField(_("Teléfono"), max_length=50, blank=True, null=True)
    email = models.EmailField(_("Correo electrónico"), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Agente Aduanal")
        verbose_name_plural = _("Agentes Aduanales")