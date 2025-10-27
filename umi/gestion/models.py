from django.db import models


# ===================== NAVIERAS =====================

class ShippingLine(models.Model):
    name = models.CharField(max_length=100)
    contact_emails = models.JSONField(default=list, blank=True)
    phone_numbers = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.name


# ===================== PUERTOS =====================

class Port(models.Model):
    PORT_TYPES = [
        ('departure', 'Departure Port'),
        ('arrival', 'Arrival Port'),
        ('transshipment', 'Transshipment Port'),
    ]

    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True, null=True)
    port_type = models.CharField(
        max_length=20,
        choices=PORT_TYPES,
        default='arrival',
        verbose_name="Port Type"
    )

    def __str__(self):
        return f"{self.name} ({self.get_port_type_display()})"


# ===================== AGENTES ADUANALES =====================

class CustomsAgent(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name


# ===================== PRODUCTOS =====================

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


# ===================== BILL OF LADING =====================

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

    # 🔹 NUEVOS CAMPOS
    departure_port = models.ForeignKey(
        Port,
        related_name='departures',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Departure Port"
    )
    arrival_port = models.ForeignKey(
        Port,
        related_name='arrivals',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Arrival Port"
    )

    def __str__(self):
        return f"BL {self.number_bl}"


# ===================== TRANSBORDOS =====================

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


# ===================== CONTENEDORES =====================

class Container(models.Model):
    bill_of_lading = models.ForeignKey(BillOfLading, on_delete=models.CASCADE, related_name="containers")
    container_number = models.CharField(max_length=50)
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.container_number


# ===================== DOCUMENTOS =====================

class Document(models.Model):
    bill_of_lading = models.ForeignKey(BillOfLading, on_delete=models.CASCADE, related_name="documents")
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to="documents/")
    expiry_date = models.DateField(blank=True, null=True, verbose_name="Expiration Date")
    is_sencamer = models.BooleanField(default=False, verbose_name="SENCAMER")
    is_rl9 = models.BooleanField(default=False, verbose_name="RL9")

    def __str__(self):
        return self.name


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

    # 🔹 CAMBIO: ahora opcional (se pueden crear pagos sin BL)
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


# ===================== PROVEEDORES =====================

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
