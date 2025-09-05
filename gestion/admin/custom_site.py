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
            context = dict(
                self.each_context(request),
                title="Dashboard UMI",
            )
            return TemplateResponse(request, "gestion_admin/dashboard.html", context)

        custom_urls = [
            path("", dashboard_view, name="dashboard"),
        ]
        return custom_urls + urls


custom_admin_site = CustomAdminSite(name="custom_admin")
custom_admin_site.index_template = "gestion_admin/dashboard.html"