from datetime import date, timedelta
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.urls import path, reverse
from django.template.response import TemplateResponse
from umi.gestion.models import (
    Container,
    PaymentPlan,
    Document,
    ShippingLine,
    BillOfLading,
    PaymentCategory,
    Supplier,
    Product,
    Port,
    CustomsAgent,
)


class CustomAdminSite(AdminSite):
    site_header = "UMI Administration"
    site_title = "UMI Admin"
    index_title = "Welcome to UMI Dashboard"

    def get_urls(self):
        urls = super().get_urls()

        def dashboard_view(request):
            today = date.today()
            upcoming_deadline = today + timedelta(days=30)

            # Metrics
            total_contenedores = Container.objects.count()
            total_navieras = ShippingLine.objects.count()
            total_facturas = PaymentPlan.objects.count()

            # Payments
            pagos_pendientes = PaymentPlan.objects.filter(status="pending").count()
            pagos_abonados = PaymentPlan.objects.filter(status="partial").count()
            pagos_pagados = PaymentPlan.objects.filter(status="paid").count()

            # Documents
            documentos_proximos = Document.objects.filter(
                expiry_date__isnull=False,
                expiry_date__lte=upcoming_deadline,
                expiry_date__gte=today
            ).count()

            documentos_vencidos = Document.objects.filter(
                expiry_date__isnull=False,
                expiry_date__lt=today
            ).count()

            # Dynamic URLs
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


class ContainerInline(admin.TabularInline):
    model = Container
    extra = 1


class DocumentInline(admin.TabularInline):
    model = Document
    extra = 1


@admin.register(BillOfLading, site=custom_admin_site)
class BillOfLadingAdmin(admin.ModelAdmin):
    list_display = ("number_bl", "invoice_number", "shipping_line", "status", "eta", "investment")
    list_filter = ("status", "shipping_line", "departure_port", "arrival_port")
    search_fields = ("number_bl", "invoice_number")

    fieldsets = (
        ("General Information", {
            "fields": ("number_bl", "invoice_number", "shipping_line", "status")
        }),
        ("Logistics", {
            "fields": ("departure_port", "arrival_port", "etd", "free_days", "eta", "customs_agent")
        }),
        ("Financial Information", {
            "fields": ("investment",)
        }),
        ("Additional Information", {
            "fields": ("additional_info",)
        }),
    )

    inlines = [ContainerInline, DocumentInline]

    class Media:
        css = {
            "all": ("gestion/css/admin_custom_styles.css",)
        
    }

@admin.register(Container, site=custom_admin_site)
class ContainerAdmin(admin.ModelAdmin):
    list_display = ("container_number", "bill_of_lading")
    search_fields = ("container_number",)
    list_filter = ("bill_of_lading__status",)


@admin.register(Document, site=custom_admin_site)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("name", "expiry_date", "bill_of_lading", "is_sencamer", "is_rl9")
    list_filter = ("is_sencamer", "is_rl9")
    search_fields = ("name",)


@admin.register(PaymentPlan, site=custom_admin_site)
class PaymentPlanAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "status", "amount", "provider")
    list_filter = ("status", "shipping_line")
    search_fields = ("invoice_number", "provider")


@admin.register(ShippingLine, site=custom_admin_site)
class ShippingLineAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(PaymentCategory, site=custom_admin_site)
class PaymentCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Supplier, site=custom_admin_site)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_person")
    search_fields = ("name", "contact_person")


@admin.register(Product, site=custom_admin_site)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("code", "description", "tariff_code")
    search_fields = ("code", "description")


@admin.register(Port, site=custom_admin_site)
class PortAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "port_type")
    list_filter = ("port_type", "country")
    search_fields = ("name", "country")


@admin.register(CustomsAgent, site=custom_admin_site)
class CustomsAgentAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email")
    search_fields = ("name", "email")
