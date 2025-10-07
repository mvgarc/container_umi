from django.contrib import admin
from gestion.admin.models_admin import custom_admin_site
from gestion.models import ShippingLine, Container, PaymentPlan, Document

@custom_admin_site.register(ShippingLine)
class ShippingLineAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_person")


@custom_admin_site.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    list_display = ("numero_contenedor", "status")


@custom_admin_site.register(PaymentPlan)
class PaymentPlanAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "status", "amount")


@custom_admin_site.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("name", "expiry_date", "required")
