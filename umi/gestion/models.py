from django.db import models
from django.utils import timezone
class ShippingLine(models.Model):
    name = models.CharField(max_length=100)
    contact_emails = models.JSONField(default=list, blank=True)  # permite varios correos
    phone_numbers = models.JSONField(default=list, blank=True)   # permite varios teléfonos

    def __str__(self):
        return self.name


class Port(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class CustomsAgent(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    code = models.CharField(max_length=50, verbose_name="Código / Modelo")
    description = models.TextField(verbose_name="Descripción del Producto")
    characteristics = models.JSONField(default=dict, blank=True)  # Ejemplo: {"color": "rojo", "dimensiones": "20x10"}
    tariff_code = models.CharField(max_length=10, verbose_name="Código Arancelario")

    def __str__(self):
        return f"{self.code} - {self.description[:30]}"


class BillOfLading(models.Model):
    STATUS_CHOICES = [
        ('transito', 'En Tránsito'),
        ('puerto', 'En Puerto'),
        ('aduana', 'En Aduana'),
        ('entregado', 'Entregado'),
        ('devuelto', 'Devuelto'),
        ('retrasado', 'Retrasado'),
        ('cancelado', 'Cancelado'),
    ]

    numero_bl = models.CharField(max_length=50, unique=True, verbose_name="Número de BL")
    invoice_number = models.CharField(max_length=50, verbose_name="Número de Factura")
    shipping_line = models.ForeignKey(ShippingLine, on_delete=models.SET_NULL, null=True, blank=True)
    etd = models.DateField(verbose_name="Fecha ETD")
    free_days = models.PositiveIntegerField(default=7)
    eta = models.DateField(verbose_name="Fecha ETA")
    additional_info = models.TextField(blank=True, null=True, verbose_name="Información Adicional")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='transito')
    investment = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Inversión / Flete")
    customs_agent = models.ForeignKey(CustomsAgent, on_delete=models.SET_NULL, null=True, blank=True)
    port = models.ForeignKey(Port, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"BL {self.numero_bl}"


class Container(models.Model):
    bill_of_lading = models.ForeignKey(BillOfLading, on_delete=models.CASCADE, related_name="containers")
    container_number = models.CharField(max_length=50)
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.container_number


class Document(models.Model):
    bill_of_lading = models.ForeignKey(BillOfLading, on_delete=models.CASCADE, related_name="documents")
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to="documents/")
    expiry_date = models.DateField(blank=True, null=True, verbose_name="Fecha de Vencimiento")
    is_sencamer = models.BooleanField(default=False)
    is_rl9 = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class PaymentCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class PaymentPlan(models.Model):
    STATUS_CHOICES = [
        ('pagado', 'Pagado'),
        ('pendiente', 'Pendiente'),
        ('abonado', 'Abonado'),
    ]

    bill_of_lading = models.ForeignKey(BillOfLading, on_delete=models.CASCADE, related_name="payments")
    invoice_number = models.CharField(max_length=50)
    invoice_date = models.DateField(verbose_name="Fecha de Factura")
    category = models.ForeignKey(PaymentCategory, on_delete=models.SET_NULL, null=True, blank=True)
    provider = models.CharField(max_length=100)
    shipping_line = models.ForeignKey(ShippingLine, on_delete=models.SET_NULL, null=True, blank=True)
    pi_number = models.CharField(max_length=50, verbose_name="Número de Producto / PI")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pendiente")
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.bill_of_lading} - {self.invoice_number}"

class Supplier(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre del proveedor")
    address = models.TextField(blank=True, null=True, verbose_name="Dirección")
    phone_numbers = models.JSONField(default=list, blank=True, verbose_name="Teléfonos")
    emails = models.JSONField(default=list, blank=True, verbose_name="Correos")
    contact_person = models.CharField(max_length=100, blank=True, null=True, verbose_name="Persona de contacto")

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ["name"]

    def __str__(self):
        return self.name
