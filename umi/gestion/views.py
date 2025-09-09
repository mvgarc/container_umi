from django.http import HttpResponse

def home(request):
    return HttpResponse("Bienvenido a la app de gestión 🚢")
