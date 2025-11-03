from django.db import models
from .shipping import ShippingLine
from .customs import CustomsAgent
from .port import Port

class BillOfLading(models.Model):
    STATUS_CHOICES = [
        ('transit', 'In Transit'),
        ('port', 'At Port'),
        ('customs', 'In Customs'),
        ('delivered', 'Delivered'),
        ('returned', 'Returned'),
        ('delayed', 'Delayed'),
        ('cancelled', 'Cancelled'),
    ]

    number_bl = models.CharField(max_length=50, unique=True, verbose_name="BL Number")
    invoice_number = models.CharField(max_length=50, verbose_name="Invoice Number")
    shipping_line = models.ForeignKey(ShippingLine, on_delete=models.SET_NULL, null=True, blank=True)
    etd = models.DateField(verbose_name="ETD Date")
    free_days = models.PositiveIntegerField(default=7, verbose_name="Free Days (7–25)")
    eta = models.DateField(verbose_name="ETA Date")
    additional_info = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='transit')
    investment = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Freight Cost / Investment")
    customs_agent = models.ForeignKey(CustomsAgent, on_delete=models.SET_NULL, null=True, blank=True)
    departure_port = models.ForeignKey(Port, related_name='departures', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Departure Port")
    arrival_port = models.ForeignKey(Port, related_name='arrivals', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Arrival Port")

    def __str__(self):
        return f"BL {self.number_bl}"