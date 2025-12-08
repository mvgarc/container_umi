from django.db import models
from django.utils.translation import gettext_lazy as _

class ShippingLine(models.Model):
    name = models.CharField(_("Nombre de la naviera"), max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Naviera")
        verbose_name_plural = _("Navieras")


class ShippingLineEmail(models.Model):
    line = models.ForeignKey(
        ShippingLine,
        related_name='contact_emails',
        on_delete=models.CASCADE,
        verbose_name=_("Naviera")
    )
    email = models.EmailField(_("Correo electrónico"))

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _("Correo de contacto")
        verbose_name_plural = _("Correos de contacto")


class ShippingLinePhone(models.Model):
    line = models.ForeignKey(
        ShippingLine,
        related_name='phone_numbers',
        on_delete=models.CASCADE,
        verbose_name=_("Naviera")
    )
    phone = models.CharField(_("Teléfono"), max_length=20)

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = _("Teléfono de contacto")
        verbose_name_plural = _("Teléfonos de contacto")