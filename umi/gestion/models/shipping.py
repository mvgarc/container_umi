from django.db import models

class ShippingLine(models.Model):
    name = models.CharField(max_length=100)
    contact_emails = models.JSONField(default=list, blank=True)
    phone_numbers = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.name