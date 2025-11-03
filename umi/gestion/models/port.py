from django.db import models

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