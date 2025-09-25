from django.contrib.admin import AdminSite
from django.urls import path
from django.template.response import TemplateResponse
from django.db.models import Sum
from django.utils.dateformat import DateFormat
from gestion.models import Container, PaymentPlan, Document, ShippingLine

class CustomAdminSite(AdminSite):
    site_header = "Panel de Administración UMI"
    site_title = "UMI Admin"
    index_title = "Bienvenido al Dashboard"

    def get_urls(self):
        urls = super().get_urls()

        def dashboard_view(request):
            total_contenedores = Container.objects.count()
            pendientes = Container.objects.filter(status="en_transito").count() 
            en_transito = Container.objects.filter(status="en_transito").count()
            entregados = Container.objects.filter(status="entregado").count()
            pagos_pendientes = PaymentPlan.objects.filter(paid=False).count()
            pagos_realizados = PaymentPlan.objects.filter(paid=True).count()
            documentos_obligatorios = Document.objects.filter(required=True).count()
            navieras = ShippingLine.objects.count()

            pagos = (
                PaymentPlan.objects.values("due_date")
                .order_by("due_date")
                .annotate(total=Sum("amount"))
            )

            pagos_labels = [DateFormat(p["due_date"]).format("d M Y") for p in pagos]
            pagos_data = [float(p["total"]) for p in pagos]
            
            context = dict(
                self.each_context(request),
                title="Dashboard UMI",
                total_contenedores=total_contenedores,
                pendientes=pendientes,
                en_transito=en_transito,
                entregados=entregados,
                pagos_pendientes=pagos_pendientes,
                pagos_realizados=pagos_realizados,
                documentos_obligatorios=documentos_obligatorios,
                navieras=navieras,
                pagos_labels=pagos_labels,
                pagos_data=pagos_data,
            )
            return TemplateResponse(request, "gestion_admin/dashboard.html", context)

        custom_urls = [
            path("", dashboard_view, name="dashboard"),
        ]
        return custom_urls + urls

custom_admin_site = CustomAdminSite(name="custom_admin")