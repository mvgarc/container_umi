from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),  # ruta básica para probar
]