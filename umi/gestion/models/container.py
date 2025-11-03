from django.db import models
from .bill_of_lading import BillOfLading
from .product import Product

class Container(models.Model):
    bill_of_lading = models.ForeignKey(BillOfLading, on_delete=models.CASCADE, related_name="containers")
    container_number = models.CharField(max_length=50)
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.container_number