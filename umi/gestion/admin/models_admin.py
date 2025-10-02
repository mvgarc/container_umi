from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import ShippingLine, Container, Document, PaymentPlan
from .resources import (
    ContainerResource, DocumentResource,
    PaymentPlanResource, ShippingLineResource
)
from .site import custom_admin_site  # tu sitio personalizado

@admin.register(ShippingLine, site=custom_admin_site)
class ShippingLineAdmin(ImportExportModelAdmin):
    resource_class = ShippingLineResource
    list_display = ('name', 'country', 'contact_email', 'phone')
    search_fields = ('name', 'country')
    ordering = ('name',)

@admin.register(Container, site=custom_admin_site)
class ContainerAdmin(ImportExportModelAdmin):
    resource_class = ContainerResource
    list_display = ('container_number', 'shipping_line', 'origin', 'eta', 'status', 'price', 'created_at')
    list_filter = ('status', 'shipping_line')
    date_hierarchy = 'created_at'
    search_fields = ('container_number', 'origin')

@admin.register(Document, site=custom_admin_site)
class DocumentAdmin(ImportExportModelAdmin):
    resource_class = DocumentResource
    list_display = ('name', 'container', 'required', 'uploaded_at')
    list_filter = ('required', 'uploaded_at')
    search_fields = ('name', 'container__container_number')

@admin.register(PaymentPlan, site=custom_admin_site)
class PaymentPlanAdmin(ImportExportModelAdmin):
    resource_class = PaymentPlanResource
    list_display = ('container', 'due_date', 'amount', 'paid')
    list_filter = ('paid', 'due_date')
    search_fields = ('container__container_number',)
