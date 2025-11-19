from django.db import models
from django.utils.translation import gettext_lazy as _

class Port(models.Model):
    PORT_TYPES = [
        ('departure', _('Puerto de salida')),
        ('arrival', _('Puerto de llegada')),
        ('transshipment', _('Puerto de transbordo')),
    ]

    name = models.CharField(_("Nombre del puerto"), max_length=100)
    country = models.CharField(_("País"), max_length=100, blank=True, null=True)
    port_type = models.CharField(
        _("Tipo de puerto"),
        max_length=20,
        choices=PORT_TYPES,
        default='arrival',
    )

    def __str__(self):
        return f"{self.name} ({self.get_port_type_display()})"

    class Meta:
        verbose_name = _("Puerto")
        verbose_name_plural = _("Puertos")
