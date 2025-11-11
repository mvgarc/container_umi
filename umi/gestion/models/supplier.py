from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    contact_person = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class SupplierPhone(models.Model):
    supplier = models.ForeignKey(
        Supplier, 
        related_name='phone_numbers', 
        on_delete=models.CASCADE
    )
    phone = models.CharField(max_length=20, verbose_name="Phone Number")

    def __str__(self):
        return self.phone

class SupplierEmail(models.Model):
    supplier = models.ForeignKey(
        Supplier, 
        related_name='emails', 
        on_delete=models.CASCADE
    )
    email = models.EmailField(verbose_name="Email Address")

    def __str__(self):
        return self.email