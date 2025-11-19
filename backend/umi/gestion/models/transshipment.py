from django.db import models
from django.utils.translation import gettext_lazy as _
from .bill_of_lading import BillOfLading
from .port import Port

class Transshipment(models.Model):
    bill_of_lading = models.ForeignKey(
        BillOfLading,
        on_delete=models.CASCADE,
        related_name='transshipments',
        verbose_name=_("Conocimiento de embarque (BL)")
    )
    port = models.ForeignKey(
        Port, 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name=_("Puerto de transbordo")
    )
    notes = models.TextField(
        _("Notas"),
        blank=True, 
        null=True
    )
    date = models.DateField(
        _("Fecha de transbordo"),
        null=True, 
        blank=True
    )

    def __str__(self):
        return f"Transbordo vía {self.port} ({self.bill_of_lading})"
    
    class Meta:
        verbose_name = _("Transbordo")
        verbose_name_plural = _("Transbordos")