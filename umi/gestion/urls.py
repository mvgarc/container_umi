from django.urls import path, include
from gestion.admin.models_admin import custom_admin_site

urlpatterns = [
    path("admin/", custom_admin_site.urls),
]