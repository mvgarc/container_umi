from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from gestion.models import (
    ShippingLine, Port, CustomsAgent, Product,
    BillOfLading, Container, Document,
    PaymentCategory, PaymentPlan, Supplier
)
from .site import custom_admin_site


# ----------------------------
# NAVIERAS (Shipping Lines)
# ----------------------------
@admin.register(ShippingLine, site=custom_admin_site)
class ShippingLineAdmin(ImportExportModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


# ----------------------------
# PUERTOS
# ----------------------------
@admin.register(Port, site=custom_admin_site)
class PortAdmin(ImportExportModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name', 'country')
    ordering = ('name',)


# ----------------------------
# AGENTES ADUANALES
# ----------------------------
@admin.register(CustomsAgent, site=custom_admin_site)
class CustomsAgentAdmin(ImportExportModelAdmin):
    list_display = ('name', 'phone', 'email')
    search_fields = ('name', 'email')
    ordering = ('name',)


# ----------------------------
# PRODUCTOS
# ----------------------------
@admin.register(Product, site=custom_admin_site)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ('code', 'description', 'tariff_code')
    search_fields = ('code', 'description', 'tariff_code')
    ordering = ('code',)


# ----------------------------
# BILL OF LADING (BL)
# ----------------------------
@admin.register(BillOfLading, site=custom_admin_site)
class BillOfLadingAdmin(ImportExportModelAdmin):
    list_display = (
        'numero_bl', 'invoice_number', 'shipping_line',
        'status', 'etd', 'eta', 'investment'
    )
    list_filter = ('status', 'shipping_line', 'customs_agent', 'port')
    search_fields = ('numero_bl', 'invoice_number')
    ordering = ('-etd',)


# ----------------------------
# CONTENEDORES
# ----------------------------
@admin.register(Container, site=custom_admin_site)
class ContainerAdmin(ImportExportModelAdmin):
    list_display = ('container_number', 'bill_of_lading')
    search_fields = ('container_number', 'bill_of_lading__numero_bl')
    ordering = ('container_number',)


# ----------------------------
# DOCUMENTOS
# ----------------------------
@admin.register(Document, site=custom_admin_site)
class DocumentAdmin(ImportExportModelAdmin):
    list_display = ('name', 'bill_of_lading', 'expiry_date', 'is_sencamer', 'is_rl9')
    list_filter = ('is_sencamer', 'is_rl9')
    search_fields = ('name', 'bill_of_lading__numero_bl')
    ordering = ('name',)


# ----------------------------
# CATEGORÍAS DE PAGO
# ----------------------------
@admin.register(PaymentCategory, site=custom_admin_site)
class PaymentCategoryAdmin(ImportExportModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


# ----------------------------
# PLAN DE PAGO
# ----------------------------
@admin.register(PaymentPlan, site=custom_admin_site)
class PaymentPlanAdmin(ImportExportModelAdmin):
    list_display = (
        'bill_of_lading', 'invoice_number', 'invoice_date',
        'category', 'provider', 'shipping_line',
        'pi_number', 'status', 'amount'
    )
    list_filter = ('status', 'category', 'shipping_line')
    search_fields = ('bill_of_lading__numero_bl', 'invoice_number', 'provider')
    ordering = ('-invoice_date',)


# ----------------------------
# PROVEEDORES
# ----------------------------
@admin.register(Supplier, site=custom_admin_site)
class SupplierAdmin(ImportExportModelAdmin):
    list_display = ('name', 'contact_person')
    search_fields = ('name', 'contact_person')
    ordering = ('name',)
