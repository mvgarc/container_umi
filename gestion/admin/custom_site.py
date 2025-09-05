from django.contrib.admin import AdminSite
from django.urls import path
from django.template.response import TemplateResponse


from gestion.models import Contenedor, PlanPago, Documento

class CustomAdminSite(AdminSite):
    site_header = "Panel de Administración UMI"
    site_title = "UMI Admin"
    index_title = "Bienvenido al Dashboard"

    def get_urls(self):
        urls = super().get_urls()

        def dashboard_view(request):
            # Obtén los datos de la base de datos
            total_contenedores = Contenedor.objects.count()
            contenedores_pendientes = Contenedor.objects.filter(estado='Pendiente').count()
            contenedores_en_transito = Contenedor.objects.filter(estado='En tránsito').count()
            contenedores_entregados = Contenedor.objects.filter(estado='Entregado').count()
            
            pagos_pendientes = PlanPago.objects.filter(pagado=False).count()
            pagos_realizados = PlanPago.objects.filter(pagado=True).count()
            
            documentos_obligatorios = Documento.objects.filter(obligatorio=True).count()

            context = dict(
                self.each_context(request),
                title="Dashboard UMI",
                total_contenedores=total_contenedores,
                pendientes=contenedores_pendientes,
                en_transito=contenedores_en_transito,
                entregados=contenedores_entregados,
                pagos_pendientes=pagos_pendientes,
                pagos_realizados=pagos_realizados,
                documentos_obligatorios=documentos_obligatorios,
            )
            return TemplateResponse(request, "gestion_admin/dashboard.html", context)

        custom_urls = [
            path("", dashboard_view, name="dashboard"),
        ]
        return custom_urls + urls

custom_admin_site = CustomAdminSite(name="custom_admin")
custom_admin_site.index_template = "gestion_admin/dashboard.html"