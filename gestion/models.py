from django.db import models
from django.contrib.auth.models import User

class Contenedor(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)
    fecha_pedido = models.DateField()
    fecha_llegada_estimada = models.DateField(null=True, blank=True)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('pendiente', 'Pendiente'),
            ('en_transito', 'En tránsito'),
            ('entregado', 'Entregado'),
        ],
        default='pendiente'
    )

    def __str__(self):
        return f"{self.codigo} - {self.estado}"


class Documento(models.Model):
    contenedor = models.ForeignKey(Contenedor, on_delete=models.CASCADE, related_name="documentos")
    nombre = models.CharField(max_length=100)
    archivo = models.FileField(upload_to='documentos/')
    obligatorio = models.BooleanField(default=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({'Obligatorio' if self.obligatorio else 'Opcional'})"


class PlanPago(models.Model):
    contenedor = models.ForeignKey(Contenedor, on_delete=models.CASCADE, related_name="pagos")
    fecha_pago = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    pagado = models.BooleanField(default=False)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Pago {self.monto} - {self.fecha_pago} ({'Pagado' if self.pagado else 'Pendiente'})"
