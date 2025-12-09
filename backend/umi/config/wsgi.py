"""
WSGI config for umi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

<<<<<<< HEAD
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'umi.config.settings')
=======
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
>>>>>>> 2a159cb1aeef995b130e2625cb58404599f7fe6a

application = get_wsgi_application()
