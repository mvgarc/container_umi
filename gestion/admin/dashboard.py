from django.contrib.admin import AdminSite
from django.urls import path
from django.shortcuts import render
from ..models import Contenedor, PlanPago

class DashboardAdminSite(AdminSite):
    site_header = "Panel de Administración"
    site_title = "UMI Admin"
    index_title = "Dashboard"

    def has_permission(self, request):
        return request.user.is_active and request.user.is_staff

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("dashboard/", self.admin_view(self.dashboard), name="dashboard"),
        ]
        return custom_urls + urls

    def dashboard(self, request):
        contenedores_pendientes = Contenedor.objects.filter(estado="pendiente").count()
        pagos_pendientes = PlanPago.objects.filter(pagado=False).count()

        context = {
            "contenedores_pendientes": contenedores_pendientes,
            "pagos_pendientes": pagos_pendientes,
        }
        return render(request, "gestion_admin/dashboard.html", context)

# Instancia de este AdminSite
custom_admin_site = DashboardAdminSite(name="custom_admin")
