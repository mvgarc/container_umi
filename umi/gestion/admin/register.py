from django.contrib import admin
from gestion.models import ShippingLine, Container, PaymentPlan, Document
from gestion.admin.custom_admin import custom_admin_site


@custom_admin_site.register(ShippingLine)
class ShippingLineAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_emails", "phone_numbers")


@custom_admin_site.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    list_display = ("container_number", "bill_of_lading")


@custom_admin_site.register(PaymentPlan)
class PaymentPlanAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "status", "amount")


@custom_admin_site.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("name", "expiry_date", "is_sencamer", "is_rl9")
