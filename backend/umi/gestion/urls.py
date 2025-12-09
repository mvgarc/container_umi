from django.urls import path
<<<<<<< HEAD

urlpatterns = []
=======
from umi.gestion.admin.custom_admin import custom_admin_site

urlpatterns = [
    path("admin/", custom_admin_site.urls),
]
>>>>>>> 2a159cb1aeef995b130e2625cb58404599f7fe6a
