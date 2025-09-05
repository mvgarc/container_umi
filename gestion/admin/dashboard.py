from django.urls import path
from django.template.response import TemplateResponse
from .custom_site import custom_admin_site

def dashboard_view(request):
    context = dict(
        custom_admin_site.each_context(request),
        title="Dashboard UMI",
    )
    return TemplateResponse(request, "gestion_admin/dashboard.html", context)

# Agregar la URL personalizada
custom_admin_site.get_urls = lambda: [
    path("", dashboard_view, name="dashboard"),
]