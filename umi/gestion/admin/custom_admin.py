from datetime import date, timedelta
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.urls import path, reverse
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _ 

from umi.gestion.models import (
    Container,
    PaymentPlan,
    PaymentCategory,
    Document,
    ShippingLine,
    ShippingLineEmail,
    ShippingLinePhone,
    BillOfLading,
    Supplier,
    SupplierPhone,
    SupplierEmail,
    Product,
    Port,
    CustomsAgent,
    CustomUser,
    PaymentAttachment,
)

from umi.gestion.admin.user_admin import CustomUserAdmin
class CustomAdminSite(AdminSite):
    site_header = _("UMI Administración")
    site_title = _("Admin UMI")
    index_title = _("Bienvenido al Panel de UMI")

    def has_permission(self, request):
        user = request.user
        return user.is_active and getattr(user, "role", None) in ["admin", "manager"]

    def get_urls(self):
        urls = super().get_urls()

        def dashboard_view(request):
            today = date.today()
            upcoming_deadline = today + timedelta(days=30)

            total_contenedores = Container.objects.count()
            total_navieras = ShippingLine.objects.count()
            total_facturas = PaymentPlan.objects.count()

            # Pagos
            pagos_pendientes = PaymentPlan.objects.filter(status="pending").count()
            pagos_abonados = PaymentPlan.objects.filter(status="partial").count()
            pagos_pagados = PaymentPlan.objects.filter(status="paid").count()

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

            urls_acceso = {
                "container_list": reverse("custom_admin:gestion_container_changelist"),
                "container_add": reverse("custom_admin:gestion_container_add"),
                "paymentplan_list": reverse("custom_admin:gestion_paymentplan_changelist"),
                "paymentplan_add": reverse("custom_admin:gestion_paymentplan_add"),
                "document_list": reverse("custom_admin:gestion_document_changelist"),
                "document_add": reverse("custom_admin:gestion_document_add"),
            }

            # Contexto del dashboard
            context = dict(
                self.each_context(request),
                title=_("Dashboard UMI"), 
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
class ShippingLineEmailInline(admin.TabularInline):
    model = ShippingLineEmail
    extra = 1 

class ShippingLinePhoneInline(admin.TabularInline):
    model = ShippingLinePhone
    extra = 1

class SupplierPhoneInline(admin.TabularInline):
    model = SupplierPhone
    extra = 1

class SupplierEmailInline(admin.TabularInline):
    model = SupplierEmail
    extra = 1

@admin.register(BillOfLading, site=custom_admin_site)
class BillOfLadingAdmin(admin.ModelAdmin):
    list_display = ("number_bl", "invoice_number", "shipping_line", "status", "eta", "investment")
    list_filter = ("status", "shipping_line", "departure_port", "arrival_port")
    search_fields = ("number_bl", "invoice_number")

    fieldsets = (
        (_("Información General"), { 
            "fields": ("number_bl", "invoice_number", "shipping_line", "status")
        }),
        (_("Logística"), {
            "fields": ("departure_port", "arrival_port", "etd", "free_days", "eta", "customs_agent")
        }),
        (_("Información Financiera"), {
            "fields": ("investment",)
        }),
        (_("Información Adicional"), {
            "fields": ("additional_info",)
        }),
    )

    inlines = [ContainerInline, DocumentInline]

    class Media:
        css = {"all": ("gestion/css/admin_custom_styles.css",)}


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


class PaymentAttachmentInline(admin.TabularInline):
    model = PaymentAttachment
    extra = 1
    fields = ('file', 'uploaded_at')
    readonly_fields = ('uploaded_at',)

@admin.register(PaymentPlan, site=custom_admin_site)
class PaymentPlanAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "status", "amount", "provider")
    list_filter = ("status", "shipping_line", "category")
    search_fields = ("invoice_number", "provider")
    inlines = [PaymentAttachmentInline]


@admin.register(ShippingLine, site=custom_admin_site)
class ShippingLineAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    inlines = [ShippingLineEmailInline, ShippingLinePhoneInline]


@admin.register(PaymentCategory, site=custom_admin_site)
class PaymentCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Supplier, site=custom_admin_site)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_person")
    search_fields = ("name", "contact_person")
    inlines = [SupplierEmailInline, SupplierPhoneInline]


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


custom_admin_site.register(CustomUser, CustomUserAdmin)