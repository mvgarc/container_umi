from django.urls import path
from django.template.response import TemplateResponse
from .custom_site import custom_admin_site


def dashboard_view(request):
    context = dict(
        custom_admin_site.each_context(request),
        title="Dashboard UMI",
    )
    return TemplateResponse(request, "gestion_admin/dashboard.html", context)


# Sobrescribir correctamente get_urls
def get_urls():
    urls = super(custom_admin_site.__class__, custom_admin_site).get_urls()
    custom_urls = [
        path("", dashboard_view, name="dashboard"),
    ]
    return custom_urls + urls


custom_admin_site.get_urls = get_urls