import json
from django.contrib.admin import AdminSite
from django.urls import path
from django.template.response import TemplateResponse
from django.db.models import Sum, Count
from django.utils.dateformat import DateFormat
from django.utils.safestring import mark_safe
from datetime import date, timedelta
from gestion.models import Container, PaymentPlan, Document, ShippingLine


class CustomAdminSite(AdminSite):
    site_header = "Panel de Administración UMI"
    site_title = "UMI Admin"
    index_title = "Bienvenido al Dashboard"

    def get_urls(self):
        urls = super().get_urls()

        def dashboard_view(request):
            # --- Métricas Generales ---
            total_contenedores = Container.objects.count()
            pagos_pendientes = PaymentPlan.objects.filter(paid=False).count()
            pagos_realizados = PaymentPlan.objects.filter(paid=True).count()
            documentos_obligatorios = Document.objects.filter(required=True).count()
            navieras = ShippingLine.objects.count()

            # --- Lógica de Documentos Vencidos/Próximos (NUEVO) ---
            today = date.today()
            upcoming_deadline = today + timedelta(days=30) # Próximo a vencer: en los próximos 30 días

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

            # --- Evolución de Pagos ---
            pagos = (
                PaymentPlan.objects.values("due_date")
                .order_by("due_date")
                .annotate(total=Sum("amount"))
            )
            pagos_labels = [DateFormat(p["due_date"]).format("d M Y") for p in pagos]
            pagos_data = [float(p["total"]) for p in pagos]
            
            # --- Pasar a JSON seguro ---
            estados_labels_json = mark_safe(json.dumps(estados_labels))
            estados_data_json = mark_safe(json.dumps(estados_data))
            pagos_labels_json = mark_safe(json.dumps(pagos_labels))
            pagos_data_json = mark_safe(json.dumps(pagos_data))

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
                estados_labels=estados_labels_json,
                estados_data=estados_data_json,
                pagos_labels=pagos_labels_json,
                pagos_data=pagos_data_json,
            )
            return TemplateResponse(request, "gestion_admin/dashboard.html", context)

        custom_urls = [
            path("", dashboard_view, name="dashboard"),
        ]
        return custom_urls + urls


custom_admin_site = CustomAdminSite(name="custom_admin")