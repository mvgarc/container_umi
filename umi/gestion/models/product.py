from django.db import models
from django.utils.translation import gettext_lazy as _

class Product(models.Model):
    code = models.CharField(_("Modelo / Código"), max_length=50)
    description = models.TextField(_("Descripción del producto"))
    tariff_code = models.CharField(_("Código arancelario"), max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.code} - {self.description[:30]}"
    
    class Meta:
        verbose_name = _("Producto")
        verbose_name_plural = _("Productos")