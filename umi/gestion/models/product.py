from django.db import models

class Product(models.Model):
    code = models.CharField(max_length=50, verbose_name="Model / Code")
    description = models.TextField(verbose_name="Product Description")
    characteristics = models.JSONField(blank=True, null=True)
    tariff_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="Tariff Code")

    def save(self, *args, **kwargs):
        if self.characteristics in [None, '']:
            self.characteristics = {}
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.description[:30]}"