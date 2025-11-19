from django.db import models
from django.utils.translation import gettext_lazy as _

class Supplier(models.Model):
    name = models.CharField(_("Nombre del proveedor"), max_length=100)
    address = models.TextField(_("Dirección"), blank=True, null=True)
    contact_person = models.CharField(_("Persona de contacto"), max_length=100, blank=True, null=True)

    class Meta:
        ordering = ["name"]
        verbose_name = _("Proveedor")
        verbose_name_plural = _("Proveedores")

    def __str__(self):
        return self.name

class SupplierPhone(models.Model):
    supplier = models.ForeignKey(
        Supplier, 
        related_name='phone_numbers', 
        on_delete=models.CASCADE,
        verbose_name=_("Proveedor")
    )
    phone = models.CharField(_("Teléfono"), max_length=20)

    def __str__(self):
        return self.phone
    
    class Meta:
        verbose_name = _("Teléfono de contacto")
        verbose_name_plural = _("Teléfonos de contacto")

class SupplierEmail(models.Model):
    supplier = models.ForeignKey(
        Supplier, 
        related_name='emails', 
        on_delete=models.CASCADE,
        verbose_name=_("Proveedor")
    )
    email = models.EmailField(_("Correo electrónico"))

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = _("Correo electrónico")
        verbose_name_plural = _("Correos electrónicos")