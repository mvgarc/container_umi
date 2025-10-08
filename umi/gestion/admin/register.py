from django.contrib import admin
from gestion.models import Container, PaymentPlan, Document, ShippingLine
from gestion.admin.custom_admin import custom_admin_site

# Registrar modelos
custom_admin_site.register(Container)
custom_admin_site.register(PaymentPlan)
custom_admin_site.register(Document)
custom_admin_site.register(ShippingLine)
