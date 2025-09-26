"""from django.contrib import admin
from gestion.models import Container, Document, PaymentPlan, ShippingLine
from .custom_site import custom_admin_site

@custom_admin_site.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    list_display = ("container_number", "shipping_line", "eta", "status", "price")
    list_filter = ("status", "shipping_line")
    search_fields = ("container_number", "shipping_line__name")

@custom_admin_site.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("name", "container", "required", "uploaded_at")
    list_filter = ("required", "uploaded_at")
    search_fields = ("name", "container__container_number")

@custom_admin_site.register(PaymentPlan)
class PaymentPlanAdmin(admin.ModelAdmin):
    list_display = ("container", "due_date", "amount", "paid")
    list_filter = ("paid", "due_date")
    search_fields = ("container__container_number",)

@custom_admin_site.register(ShippingLine)
class ShippingLineAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "contact_email")
    search_fields = ("name", "country")
"""