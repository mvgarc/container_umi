from django.db import models
from django.utils.translation import gettext_lazy as _
from .bill_of_lading import BillOfLading
from .product import Product

class Container(models.Model):
    bill_of_lading = models.ForeignKey(
        BillOfLading, 
        on_delete=models.CASCADE, 
        related_name="containers",
        verbose_name=_("Conocimiento de embarque (BL)")
    )
    container_number = models.CharField(_("Número de contenedor"), max_length=50)
    products = models.ManyToManyField(
        Product, 
        blank=True,
        verbose_name=_("Productos")
    )

    def __str__(self):
        return self.container_number
    
    class Meta:
        verbose_name = _("Contenedor")
        verbose_name_plural = _("Contenedores")