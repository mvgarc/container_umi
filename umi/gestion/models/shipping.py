from django.db import models
class ShippingLine(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ShippingLineEmail(models.Model):
    line = models.ForeignKey(ShippingLine, related_name='contact_emails', on_delete=models.CASCADE)
    email = models.EmailField()

    def __str__(self):
        return self.email

class ShippingLinePhone(models.Model):
    line = models.ForeignKey(ShippingLine, related_name='phone_numbers', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.phone