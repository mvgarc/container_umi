from datetime import date, timedelta
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.urls import path, reverse
from django.template.response import TemplateResponse
from gestion.models import (
    Container,
    PaymentPlan,
    Document,
    ShippingLine,
    BillOfLading,
    PaymentCategory,
    Supplier,
)


class CustomAdminSite(AdminSite):
    site_header = "Panel de Administración UMI"
    site_title = "UMI Admin"
    index_title = "Bienvenido al Dashboard"

    def get_urls(self):
        urls = super().get_urls()

        def dashboard_view(request):
            today = date.today()
            upcoming_deadline = today + timedelta(days=30)

            # Métricas principales
            total_contenedores = Container.objects.count()
            total_navieras = ShippingLine.objects.count()
            total_facturas = PaymentPlan.objects.count()

            # Pagos
            pagos_pendientes = PaymentPlan.objects.filter(status="pendiente").count()
            pagos_abonados = PaymentPlan.objects.filter(status="abonado").count()
            pagos_pagados = PaymentPlan.objects.filter(status="pagado").count()

            # Documentos
            documentos_proximos = Document.objects.filter(
                expiry_date__isnull=False,
                expiry_date__lte=upcoming_deadline,
                expiry_date__gte=today
            ).count()

            documentos_vencidos = Document.objects.filter(
                expiry_date__isnull=False,
                expiry_date__lt=today
            ).count()

            # URLs dinámicas
            urls_acceso = {
                "container_list": reverse("custom_admin:gestion_container_changelist"),
                "container_add": reverse("custom_admin:gestion_container_add"),
                "paymentplan_list": reverse("custom_admin:gestion_paymentplan_changelist"),
                "paymentplan_add": reverse("custom_admin:gestion_paymentplan_add"),
                "document_list": reverse("custom_admin:gestion_document_changelist"),
                "document_add": reverse("custom_admin:gestion_document_add"),
            }

            context = dict(
                self.each_context(request),
                title="Dashboard UMI",
                total_contenedores=total_contenedores,
                total_navieras=total_navieras,
                total_facturas=total_facturas,
                pagos_pendientes=pagos_pendientes,
                pagos_abonados=pagos_abonados,
                pagos_realizados=pagos_pagados,
                documentos_proximos=documentos_proximos,
                documentos_vencidos=documentos_vencidos,
                **urls_acceso
            )

            return TemplateResponse(request, "admin/dashboard.html", context)

        custom_urls = [path("", self.admin_view(dashboard_view), name="dashboard")]
        return custom_urls + urls


custom_admin_site = CustomAdminSite(name="custom_admin")

# ========== MODELOS REGISTRADOS ==========

@admin.register(ShippingLine, site=custom_admin_site)
class ShippingLineAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Container, site=custom_admin_site)
class ContainerAdmin(admin.ModelAdmin):
    list_display = ("container_number", "bill_of_lading")
    search_fields = ("container_number",)
    list_filter = ("bill_of_lading__status",)


@admin.register(PaymentPlan, site=custom_admin_site)
class PaymentPlanAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "status", "amount", "provider")
    list_filter = ("status", "shipping_line")
    search_fields = ("invoice_number", "provider")


@admin.register(Document, site=custom_admin_site)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("name", "expiry_date", "bill_of_lading")
    list_filter = ("is_sencamer", "is_rl9")
    search_fields = ("name",)


@admin.register(BillOfLading, site=custom_admin_site)
class BillOfLadingAdmin(admin.ModelAdmin):
    list_display = ("numero_bl", "invoice_number", "status", "eta", "shipping_line")
    list_filter = ("status", "shipping_line")
    search_fields = ("numero_bl", "invoice_number")


@admin.register(PaymentCategory, site=custom_admin_site)
class PaymentCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Supplier, site=custom_admin_site)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_person")
    search_fields = ("name", "contact_person")
