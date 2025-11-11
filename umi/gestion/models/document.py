from django.db import models
from .bill_of_lading import BillOfLading

class Document(models.Model):
    bill_of_lading = models.ForeignKey(BillOfLading, on_delete=models.CASCADE, related_name="documents", verbose_name="Documentos")
    name = models.CharField(verbose_name="Nombre", max_length=100)
    file = models.FileField(upload_to="documents/", verbose_name="Archivo")
    expiry_date = models.DateField(blank=True, null=True, verbose_name="Vencimiento")
    is_sencamer = models.BooleanField(default=False, verbose_name="SENCAMER")
    is_rl9 = models.BooleanField(default=False, verbose_name="RL9")

    def __str__(self):
        return self.name
