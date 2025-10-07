from datetime import date, timedelta
from django.contrib.admin import AdminSite
from django.urls import path, reverse
from django.template.response import TemplateResponse
from gestion.models import Container, PaymentPlan, Document, ShippingLine


class CustomAdminSite(AdminSite):
    site_header = "Panel de Administración UMI"
    site_title = "UMI Admin"
    index_title = "Bienvenido al Dashboard"

    def get_urls(self):
        default_urls = super().get_urls()

        def dashboard_view(request):
            # --- MÉTRICAS GENERALES ---
            total_contenedores = Container.objects.count()
            navieras = ShippingLine.objects.count()

            # --- ESTADO DE PAGOS ---
            pagos_pendientes = PaymentPlan.objects.filter(status="pendiente").count()
            pagos_abonados = PaymentPlan.objects.filter(status="abonado").count()
            pagos_realizados = PaymentPlan.objects.filter(status="pagado").count()

            # --- DOCUMENTOS PRÓXIMOS A VENCER Y VENCIDOS ---
            today = date.today()
            upcoming_deadline = today + timedelta(days=30)

            documentos_proximos = Document.objects.filter(
                expiry_date__isnull=False,
                expiry_date__lte=upcoming_deadline,
                expiry_date__gte=today
            ).count()

            documentos_vencidos = Document.objects.filter(
                expiry_date__isnull=False,
                expiry_date__lt=today
            ).count()

            # --- URLs DINÁMICAS PARA ENLACES ---
            urls_acceso = {
                "container_list": reverse(f"custom_admin:{Container._meta.app_label}_{Container._meta.model_name}_changelist"),
                "container_add": reverse(f"custom_admin:{Container._meta.app_label}_{Container._meta.model_name}_add"),
                "paymentplan_list": reverse(f"custom_admin:{PaymentPlan._meta.app_label}_{PaymentPlan._meta.model_name}_changelist"),
                "paymentplan_add": reverse(f"custom_admin:{PaymentPlan._meta.app_label}_{PaymentPlan._meta.model_name}_add"),
            }

            # --- CONTEXTO PARA EL TEMPLATE ---
            context = dict(
                self.each_context(request),
                title="Dashboard UMI",
                total_contenedores=total_contenedores,
                pagos_pendientes=pagos_pendientes,
                pagos_abonados=pagos_abonados,
                pagos_realizados=pagos_realizados,
                documentos_proximos=documentos_proximos,
                documentos_vencidos=documentos_vencidos,
                navieras=navieras,
                **urls_acceso
            )

            return TemplateResponse(request, "admin/dashboard.html", context)

        custom_urls = [path("", dashboard_view, name="dashboard")]
        return custom_urls + default_urls


custom_admin_site = CustomAdminSite(name="custom_admin")
