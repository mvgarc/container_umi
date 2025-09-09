from django.contrib.admin import AdminSite
from django.urls import path
from django.template.response import TemplateResponse
from gestion.models import Container, PaymentPlan, Document, ShippingLine

class CustomAdminSite(AdminSite):
    site_header = "Panel de Administración UMI"
    site_title = "UMI Admin"
    index_title = "Bienvenido al Dashboard"

    def get_urls(self):
        urls = super().get_urls()

        def dashboard_view(request):
            context = dict(
                self.each_context(request),
                title="Dashboard UMI",
                total_contenedores=Container.objects.count(),
                pendientes=Container.objects.filter(status="pendiente").count(),
                en_transito=Container.objects.filter(status="en_transito").count(),
                entregados=Container.objects.filter(status="entregado").count(),
                pagos_pendientes=PaymentPlan.objects.filter(paid=False).count(),
                pagos_realizados=PaymentPlan.objects.filter(paid=True).count(),
                documentos_obligatorios=Document.objects.filter(required=True).count(),
                navieras=ShippingLine.objects.count(),
            )
            return TemplateResponse(request, "gestion_admin/dashboard.html", context)

        custom_urls = [
            path("", dashboard_view, name="dashboard"),
        ]
        return custom_urls + urls

custom_admin_site = CustomAdminSite(name="custom_admin")
