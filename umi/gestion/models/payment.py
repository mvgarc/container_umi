from django.db import models
from .bill_of_lading import BillOfLading
from .shipping import ShippingLine


# ===================== CATEGORÍAS DE PAGO =====================

class PaymentCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# ===================== PLANES / PAGOS =====================

class PaymentPlan(models.Model):
    STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('partial', 'Partially Paid'),
    ]

    bill_of_lading = models.ForeignKey(
        BillOfLading,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments"
    )
    invoice_number = models.CharField(max_length=50)
    invoice_date = models.DateField(verbose_name="Invoice Date")
    category = models.ForeignKey(PaymentCategory, on_delete=models.SET_NULL, null=True, blank=True)
    provider = models.CharField(max_length=100)
    shipping_line = models.ForeignKey(ShippingLine, on_delete=models.SET_NULL, null=True, blank=True)
    pi_number = models.CharField(max_length=50, verbose_name="PI / Product Number")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.invoice_number} - {self.provider}"


# ===================== RESPALDOS DE PAGO =====================

class PaymentAttachment(models.Model):
    payment = models.ForeignKey(PaymentPlan, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='payment_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.payment.invoice_number}"
