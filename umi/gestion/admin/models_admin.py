from django.contrib import admin
from .models import (
    BillOfLading,
    Container,
    Document,
    Product,
    Supplier,
    ShippingLine,
    PaymentPlan,
    PaymentCategory,
    Port,
    CustomsAgent,
)

# =============== NAVIERAS ===============
@admin.register(ShippingLine)
class ShippingLineAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


# =============== PROVEEDORES ===============
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_person")
    search_fields = ("name", "contact_person")
    ordering = ("name",)


# =============== PRODUCTOS ===============
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("codigo", "producto", "codigo_arancelario")
    search_fields = ("codigo", "producto", "codigo_arancelario")
    ordering = ("codigo",)


# =============== PUERTOS ===============
@admin.register(Port)
class PortAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


# =============== AGENTES ADUANALES ===============
@admin.register(CustomsAgent)
class CustomsAgentAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


# =============== CATEGORÍAS DE PAGO ===============
@admin.register(PaymentCategory)
class PaymentCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


# =============== DOCUMENTOS ===============
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("name", "bl", "expiry_date", "uploaded_at")
    list_filter = ("expiry_date",)
    search_fields = ("name", "bl__numero_bl")
    ordering = ("-uploaded_at",)


# =============== CONTENEDORES ===============
@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    list_display = ("numero_contenedor", "bill_of_lading", "created_at")
    search_fields = ("numero_contenedor", "bill_of_lading__numero_bl")
    ordering = ("-created_at",)


# =============== BL (Bill of Lading) ===============
@admin.register(BillOfLading)
class BillOfLadingAdmin(admin.ModelAdmin):
    list_display = (
        "numero_bl",
        "numero_factura",
        "naviera",
        "estatus",
        "eta",
        "etd",
        "inversion",
    )
    list_filter = ("estatus", "naviera")
    search_fields = ("numero_bl", "numero_factura")
    ordering = ("-eta",)


# =============== PLAN DE PAGO ===============
@admin.register(PaymentPlan)
class PaymentPlanAdmin(admin.ModelAdmin):
    list_display = (
        "bl",
        "numero_factura",
        "fecha_factura",
        "categoria",
        "proveedor",
        "naviera",
        "status",
        "monto",
    )
    list_filter = ("status", "categoria", "naviera")
    search_fields = ("numero_factura", "bl__numero_bl")
    ordering = ("-fecha_factura",)
