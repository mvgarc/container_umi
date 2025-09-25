from django.contrib import admin
from gestion.models import ShippingLine, Container, Document, PaymentPlan
from .site import custom_admin_site  # tu sitio personalizado

@admin.register(ShippingLine, site=custom_admin_site)
class ShippingLineAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'contact_email', 'phone')
    search_fields = ('name', 'country')
    ordering = ('name',)

@admin.register(Container, site=custom_admin_site)
class ContainerAdmin(admin.ModelAdmin):
    list_display = ('container_number', 'shipping_line', 'origin', 'eta', 'status', 'price', 'created_at')
    list_filter = ('status', 'shipping_line')
    date_hierarchy = 'created_at'
    search_fields = ('container_number', 'origin')

@admin.register(Document, site=custom_admin_site)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'container', 'required', 'uploaded_at')
    list_filter = ('required', 'uploaded_at')
    search_fields = ('name', 'container__container_number')

@admin.register(PaymentPlan, site=custom_admin_site)
class PaymentPlanAdmin(admin.ModelAdmin):
    list_display = ('container', 'due_date', 'amount', 'paid')
    list_filter = ('paid', 'due_date')
    search_fields = ('container__container_number',)
