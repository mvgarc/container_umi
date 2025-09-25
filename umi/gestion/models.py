from django.db import models

class ShippingLine(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la naviera")
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name="País de origen")
    contact_email = models.EmailField(blank=True, null=True, verbose_name="Correo de contacto")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    website = models.URLField(blank=True, null=True, verbose_name="Sitio web")

    class Meta:
        verbose_name = "Naviera"
        verbose_name_plural = "Navieras"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Container(models.Model):
    STATUS_CHOICES = [
        ("en_transito", "En tránsito"),
        ("en_puerto", "En puerto"),
        ("en_aduana", "En aduana"),
        ("entregado", "Entregado"),
        ("devuelto", "Devuelto"),
        ("retrasado", "Retrasado"),
    ]

    container_number = models.CharField(max_length=11, unique=True, verbose_name="Número de contenedor")
    shipping_line = models.ForeignKey(ShippingLine, on_delete=models.CASCADE, related_name="containers", verbose_name="Naviera")
    origin = models.CharField(max_length=100, verbose_name="Origen")
    eta = models.DateField(verbose_name="Fecha estimada de arribo (ETA)")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="Estado")
    documentation = models.FileField(upload_to="documents/", blank=True, null=True, verbose_name="Documentación")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contenedor"
        verbose_name_plural = "Contenedores"

    def __str__(self):
        return f"{self.container_number} - {self.status}"


class Document(models.Model):
    container = models.ForeignKey(Container, on_delete=models.CASCADE, related_name="documents")
    name = models.CharField(max_length=100, verbose_name="Nombre del documento")
    file = models.FileField(upload_to="documents/")
    required = models.BooleanField(default=True, verbose_name="Es obligatorio")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateField(blank=True, null=True, verbose_name="Fecha de vencimiento") 

    def __str__(self):
        return f"{self.name} ({'Obligatorio' if self.required else 'Opcional'})"


class PaymentPlan(models.Model):
    container = models.ForeignKey(Container, on_delete=models.CASCADE, related_name="payments")
    due_date = models.DateField(verbose_name="Fecha de pago")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto")
    paid = models.BooleanField(default=False, verbose_name="Pagado")
    notes = models.TextField(blank=True, verbose_name="Observaciones")

    def __str__(self):
        return f"Pago {self.amount} - {self.due_date} ({'Pagado' if self.paid else 'Pendiente'})"