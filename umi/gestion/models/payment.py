from django.db import models
from django.utils.translation import gettext_lazy as _
from .bill_of_lading import BillOfLading
from .shipping import ShippingLine
import os

class PaymentCategory(models.Model):
    name = models.CharField(_("Nombre de la categoría"), max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Categoría de pago")
        verbose_name_plural = _("Categorías de pago")


class PaymentPlan(models.Model):
    STATUS_CHOICES = [
        ('paid', _('Pagado')),
        ('pending', _('Pendiente')),
        ('partial', _('Parcialmente Pagado')),
    ]

    bill_of_lading = models.ForeignKey(
        BillOfLading,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
        verbose_name=_("Conocimiento de embarque (BL)")
    )
    invoice_number = models.CharField(_("Número de factura"), max_length=50)
    invoice_date = models.DateField(_("Fecha de factura"))
    category = models.ForeignKey(
        PaymentCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name=_("Categoría")
    )
    provider = models.CharField(_("Proveedor / Acreedor"), max_length=100)
    shipping_line = models.ForeignKey(
        ShippingLine, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name=_("Naviera")
    )
    pi_number = models.CharField(_("Número PI / Producto"), max_length=50)
    status = models.CharField(_("Estado de pago"), max_length=20, choices=STATUS_CHOICES, default="pending")
    amount = models.DecimalField(_("Monto total"), max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.invoice_number} - {self.provider}"
    
    class Meta:
        verbose_name = _("Plan de Pago")
        verbose_name_plural = _("Planes de Pago")

class PaymentAttachment(models.Model):
    payment = models.ForeignKey(
        PaymentPlan, 
        on_delete=models.CASCADE, 
        related_name='attachments',
        verbose_name=_("Pago asociado")
    )
    file = models.FileField(_("Archivo"), upload_to='payment_attachments/')
    uploaded_at = models.DateTimeField(_("Fecha de subida"), auto_now_add=True)

    def __str__(self):
        return f"Adjunto para {self.payment.invoice_number}"

    def file_name(self):
        return os.path.basename(self.file.name)

    def file_url(self):
        return self.file.url
    
    class Meta:
        verbose_name = _("Adjunto de Pago")
        verbose_name_plural = _("Adjuntos de Pago")