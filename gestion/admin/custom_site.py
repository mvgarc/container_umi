from django.contrib.admin import AdminSite

class CustomAdminSite(AdminSite):
    site_header = "Panel de Administración UMI"
    site_title = "UMI Admin"
    index_title = "Bienvenido al Dashboard"

custom_admin_site = CustomAdminSite(name="custom_admin")
