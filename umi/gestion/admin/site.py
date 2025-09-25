from django.contrib.admin import AdminSite
class CustomAdminSite(AdminSite):
    site_header = 'Administración UMI Personalizada'
    site_title = 'Portal de Gestión UMI'
    index_title = 'Bienvenido al Administrador UMI'
    
custom_admin_site = CustomAdminSite(name='customadmin')