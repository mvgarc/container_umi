from django.db import models
from django.utils.translation import gettext_lazy as _
from .bill_of_lading import BillOfLading

class Document(models.Model):
    bill_of_lading = models.ForeignKey(
        BillOfLading, 
        on_delete=models.CASCADE, 
        related_name="documents", 
        verbose_name=_("Conocimiento de embarque (BL)")
    )
    name = models.CharField(_("Nombre del documento"), max_length=100)
    file = models.FileField(_("Archivo"), upload_to="documents/")
    expiry_date = models.DateField(_("Fecha de vencimiento"), blank=True, null=True)
    is_sencamer = models.BooleanField(_("SENCAMER"), default=False)
    is_rl9 = models.BooleanField(_("RL9"), default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Documento")
        verbose_name_plural = _("Documentos")