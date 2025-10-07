import logging
from .models_admin import custom_admin_site

def register_admin_models():
    """Importa los modelos de admin sin causar bucles de importación."""
    try:
        from . import register_models
        logging.info("Modelos registrados correctamente en el custom_admin_site.")
    except Exception as e:
        logging.warning(f"No se pudo cargar register_models todavía: {e}")

# Ejecutar registro explícitamente
register_admin_models()
