from django.contrib import admin
from .dashboard import custom_admin_site
from ..models import Contenedor, Documento, PlanPago

@custom_admin_site.register(Contenedor)
class ContenedorAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion', 'fecha_pedido', 'fecha_llegada_estimada', 'estado')
    list_filter = ('estado', 'fecha_pedido', 'fecha_llegada_estimada')
    search_fields = ('codigo', 'descripcion')
    ordering = ('-fecha_pedido',)


@custom_admin_site.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'contenedor', 'obligatorio', 'fecha_subida')
    list_filter = ('obligatorio', 'fecha_subida')
    search_fields = ('nombre', 'contenedor__codigo')
    date_hierarchy = 'fecha_subida'


@custom_admin_site.register(PlanPago)
class PlanPagoAdmin(admin.ModelAdmin):
    list_display = ('contenedor', 'fecha_pago', 'monto', 'pagado')
    list_filter = ('pagado', 'fecha_pago')
    search_fields = ('contenedor__codigo',)
    date_hierarchy = 'fecha_pago'
    ordering = ('fecha_pago',)
