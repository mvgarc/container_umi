from django.urls import path
from umi.gestion.admin.custom_admin import custom_admin_site
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", custom_admin_site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
