"""
ASGI config for umi project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

<<<<<<< HEAD
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'umi.config.settings')
=======
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
>>>>>>> 2a159cb1aeef995b130e2625cb58404599f7fe6a

application = get_asgi_application()
