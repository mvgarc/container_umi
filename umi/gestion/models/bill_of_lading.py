from django.db import models
from django.utils.translation import gettext_lazy as _
from .shipping import ShippingLine
from .customs import CustomsAgent
from .port import Port

class BillOfLading(models.Model):
    STATUS_CHOICES = [
        ('transit', _('En Tránsito')),
        ('port', _('En Puerto')),
        ('customs', _('En Aduana')),
        ('delivered', _('Entregado')),
        ('returned', _('Devuelto')),
        ('delayed', _('Retrasado')),
        ('cancelled', _('Cancelado')),
    ]

    number_bl = models.CharField(_("Número BL"), max_length=50, unique=True)
    invoice_number = models.CharField(_("Número de factura"), max_length=50)
    shipping_line = models.ForeignKey(
        ShippingLine, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name=_("Naviera")
    )
    etd = models.DateField(_("Fecha ETD (Salida)"), auto_now_add=False)
    free_days = models.PositiveIntegerField(_("Días libres"), default=7)
    eta = models.DateField(_("Fecha ETA (Llegada)"), auto_now_add=False)
    additional_info = models.TextField(_("Información adicional"), blank=True, null=True)
    status = models.CharField(_("Estado"), max_length=20, choices=STATUS_CHOICES, default='transit')
    investment = models.DecimalField(_("Costo de flete / Inversión"), max_digits=12, decimal_places=2)
    customs_agent = models.ForeignKey(
        CustomsAgent, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name=_("Agente aduanal")
    )
    departure_port = models.ForeignKey(
        Port, 
        related_name='departures', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name=_("Puerto de salida")
    )
    arrival_port = models.ForeignKey(
        Port, 
        related_name='arrivals', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name=_("Puerto de llegada")
    )

    def __str__(self):
        return f"BL {self.number_bl}"

    class Meta:
        verbose_name = _("Conocimiento de Embarque (BL)")
        verbose_name_plural = _("Conocimientos de Embarque (BL)")