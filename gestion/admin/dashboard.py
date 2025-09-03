from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _

class DashboardAdminSite(AdminSite):
    site_header = "Panel de Administración"
    site_title = "UMI Admin"
    index_title = "Dashboard"

    def has_permission(self, request):
        """
        Permite acceso a cualquier usuario activo y staff.
        Los superusuarios también entran aquí.
        """
        return request.user.is_active and request.user.is_staff


custom_admin_site = DashboardAdminSite(name="custom_admin")
