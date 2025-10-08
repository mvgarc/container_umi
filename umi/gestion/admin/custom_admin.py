from datetime import date, timedelta
from django.contrib import admin
from django.urls import path, reverse
from django.template.response import TemplateResponse
from gestion.models import Container, PaymentPlan, Document, ShippingLine


class CustomAdminSite(admin.AdminSite):
    site_header = "Panel de Administración UMI"
    site_title = "UMI Admin"
    index_title = "Bienvenido al Dashboard"

    def get_urls(self):
        default_urls = super().get_urls()

        def dashboard_view(request):
            # --- MÉTRICAS ---
            total_contenedores = Container.objects.count()
            navieras = ShippingLine.objects.count()

            pagos_pendientes = PaymentPlan.objects.filter(status="pendiente").count()
            pagos_abonados = PaymentPlan.objects.filter(status="abonado").count()
            pagos_pagados = PaymentPlan.objects.filter(status="pagado").count()

            today = date.today()
            upcoming = today + timedelta(days=30)

            docs_proximos = Document.objects.filter(
                expiry_date__range=(today, upcoming)
            ).count()
            docs_vencidos = Document.objects.filter(
                expiry_date__lt=today
            ).count()

            context = dict(
                self.each_context(request),
                title="Dashboard UMI",
                total_contenedores=total_contenedores,
                navieras=navieras,
                pagos_pendientes=pagos_pendientes,
                pagos_abonados=pagos_abonados,
                pagos_pagados=pagos_pagados,
                docs_proximos=docs_proximos,
                docs_vencidos=docs_vencidos,
            )

            return TemplateResponse(request, "admin/dashboard.html", context)

        custom_urls = [path("", dashboard_view, name="dashboard")]
        return custom_urls + default_urls


custom_admin_site = CustomAdminSite(name="custom_admin")
