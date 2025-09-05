from .custom_site import CustomAdminSite

custom_admin_site = CustomAdminSite(name="custom_admin")
custom_admin_site.index_template = "gestion_admin/dashboard.html"
from . import base
from . import dashboard