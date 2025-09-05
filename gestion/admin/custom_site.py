from django.contrib.admin import AdminSite
from django.urls import path
from django.template.response import TemplateResponse

class CustomAdminSite(AdminSite):
    site_header = "Panel de Administración UMI"
    site_title = "UMI Admin"
    index_title = "Bienvenido al Dashboard"

    def get_urls(self):
        urls = super().get_urls()

        def dashboard_view(request):
            # Importamos aquí para evitar errores circulares
            from gestion.models import Contenedor, PlanPago, Documento

            total_contenedores = Contenedor.objects.count()
            pendientes = Contenedor.objects.filter(estado="pendiente").count()
            en_transito = Contenedor.objects.filter(estado="en_transito").count()
            entregados = Contenedor.objects.filter(estado="entregado").count()

            pagos_pendientes = PlanPago.objects.filter(pagado=False).count()
            pagos_realizados = PlanPago.objects.filter(pagado=True).count()
            documentos_obligatorios = Documento.objects.filter(obligatorio=True).count()

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
            )
            return TemplateResponse(request, "gestion_admin/dashboard.html", context)

        custom_urls = [
            path("", dashboard_view, name="dashboard"),
        ]
        return custom_urls + urls
