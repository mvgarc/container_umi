from django.urls import path
from umi.gestion.admin.custom_admin import custom_admin_site

urlpatterns = [
    path("admin/", custom_admin_site.urls),
]
