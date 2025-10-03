import json
from datetime import date, timedelta
from django.contrib.admin import AdminSite
from django.urls import path, reverse
from django.template.response import TemplateResponse
from django.db.models import Sum, Count
from django.utils.dateformat import DateFormat
from gestion.models import Container, PaymentPlan, Document, ShippingLine


class CustomAdminSite(AdminSite):
    site_header = "Panel de Administración UMI"
    site_title = "UMI Admin"
    index_title = "Bienvenido al Dashboard"

    def get_urls(self):
        default_urls = super().get_urls()

        def dashboard_view(request):
            # --- Métricas Generales ---
            total_contenedores = Container.objects.count()
            pagos_pendientes = PaymentPlan.objects.filter(paid=False).count()
            pagos_realizados = PaymentPlan.objects.filter(paid=True).count()
            documentos_obligatorios = Document.objects.filter(required=True).count()
            navieras = ShippingLine.objects.count()

            # --- Documentos vencidos / próximos ---
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

            # --- Contenedores por estado ---
            estados_data_raw = (
                Container.objects.values("status")
                .annotate(total=Count("id"))
                .order_by("status")
            )
            status_map = {
                'en_transito': 'En Tránsito',
                'en_puerto': 'En Puerto',
                'en_aduana': 'En Aduana',
                'entregado': 'Entregado',
                'devuelto': 'Devuelto',
                'retrasado': 'Retrasado',
            }
            estados_labels = [status_map.get(c['status'], c['status']) for c in estados_data_raw]
            estados_data = [c['total'] for c in estados_data_raw]

            # --- Evolución de pagos ---
            pagos = (
                PaymentPlan.objects.filter(paid=True).values("due_date")
                .order_by("due_date")
                .annotate(total=Sum("amount"))
            )
            pagos_labels = [DateFormat(p["due_date"]).format("d M Y") for p in pagos]
            pagos_data = [float(p["total"]) for p in pagos]

            # --- Datos de barra ---
            pagos_pendientes_data = [pagos_pendientes]
            pagos_realizados_data = [pagos_realizados]

            # Generar URLs dinámicamente
            urls_acceso = {
                "container_list": reverse(f"custom_admin:{Container._meta.app_label}_{Container._meta.model_name}_changelist"),
                "container_add": reverse(f"custom_admin:{Container._meta.app_label}_{Container._meta.model_name}_add"),
                "document_list": reverse(f"custom_admin:{Document._meta.app_label}_{Document._meta.model_name}_changelist"),
                "document_add": reverse(f"custom_admin:{Document._meta.app_label}_{Document._meta.model_name}_add"),
                "shippingline_list": reverse(f"custom_admin:{ShippingLine._meta.app_label}_{ShippingLine._meta.model_name}_changelist"),
                "shippingline_add": reverse(f"custom_admin:{ShippingLine._meta.app_label}_{ShippingLine._meta.model_name}_add"),
                "paymentplan_list": reverse(f"custom_admin:{PaymentPlan._meta.app_label}_{PaymentPlan._meta.model_name}_changelist"),
                "paymentplan_add": reverse(f"custom_admin:{PaymentPlan._meta.app_label}_{PaymentPlan._meta.model_name}_add"),
            }

            context = dict(
                self.each_context(request),
                title="Dashboard UMI",
                total_contenedores=total_contenedores,
                pagos_pendientes=pagos_pendientes,
                pagos_realizados=pagos_realizados,
                documentos_obligatorios=documentos_obligatorios,
                navieras=navieras,
                documentos_proximos=documentos_proximos,
                documentos_vencidos=documentos_vencidos,
                estados_labels=estados_labels,
                estados_data=estados_data,
                pagos_labels=pagos_labels,
                pagos_data=pagos_data,
                pagos_pendientes_data=pagos_pendientes_data,
                pagos_realizados_data=pagos_realizados_data,
                **urls_acceso
            )
            return TemplateResponse(request, "gestion_admin/dashboard.html", context)

        custom_urls = [path("", dashboard_view, name="dashboard")]
        return custom_urls + default_urls


custom_admin_site = CustomAdminSite(name="custom_admin")
