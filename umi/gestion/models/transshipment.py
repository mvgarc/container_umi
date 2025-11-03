from django.db import models
from .bill_of_lading import BillOfLading
from .port import Port

class Transshipment(models.Model):
    bill_of_lading = models.ForeignKey(
        BillOfLading,
        on_delete=models.CASCADE,
        related_name='transshipments'
    )
    port = models.ForeignKey(Port, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True, null=True)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Transshipment via {self.port} ({self.bill_of_lading})"
