from django.http import HttpResponse
from django.shortcuts import render
from umi.gestion.decorators import role_required

# Vista principal
def home(request):
    return HttpResponse("Bienvenido a la app de gestión")

# Dashboard general (acceso amplio)
@role_required(['admin', 'manager', 'operator', 'viewer' ])
def dashboard_view(request):
    return render(request, 'admin/dashboard.html')

# Gestión de contenedores
@role_required(['admin', 'manager'])
def containers_view(request):
    return render(request, 'gestion/containers.html')

# Gestión de pagos
@role_required(['admin', 'manager'])
def payments_view(request):
    return render(request, 'gestion/payments.html')

# Vista de reportes (solo lectura)
@role_required(['viewer', 'manager', 'admin'])
def reports_view(request):
    return render(request, 'gestion/reports.html')
