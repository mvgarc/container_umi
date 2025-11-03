from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    phone_numbers = models.JSONField(default=list, blank=True)
    emails = models.JSONField(default=list, blank=True)
    contact_person = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
