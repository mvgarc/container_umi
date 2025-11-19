from pathlib import Path
import os
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================
# CONFIGURACIÓN DE SEGURIDAD
# ============================================================

SECRET_KEY = os.getenv("SECRET_KEY", "clave_insegura_dev")

DEBUG = False if os.getenv("DJANGO_ENV") == "production" else True

ALLOWED_HOSTS = ['.elasticbeanstalk.com', '*']


# ============================================================
# APLICACIONES
# ============================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "umi.gestion",
    "django_extensions",
    "import_export",
    'rest_framework',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "umi.config.urls"
WSGI_APPLICATION = "umi.config.wsgi.application"

# ============================================================
# MODELO DE USUARIO PERSONALIZADO
# ============================================================

AUTH_USER_MODEL = "gestion.CustomUser"


# ============================================================
# BASE DE DATOS (SQLite en local / PostgreSQL en producción)
# ============================================================

if os.getenv("USE_POSTGRES", "False") == "True":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
            "HOST": os.getenv("DB_HOST"),
            "PORT": os.getenv("DB_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# ============================================================
# VALIDACIÓN DE CONTRASEÑAS
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ============================================================
# INTERNACIONALIZACIÓN
# ============================================================

LANGUAGE_CODE = 'es'
TIME_ZONE = "America/Caracas"
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('es', _('Español')),
    ('en', _('Inglés')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# ============================================================
# ARCHIVOS ESTÁTICOS Y MEDIA
# ============================================================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "gestion" / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# ============================================================
# AUTENTICACIÓN Y LOGIN
# ============================================================

LOGIN_URL = "/"
LOGOUT_REDIRECT_URL = "/"
LOGIN_REDIRECT_URL = "/"


# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "gestion" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ============================================================
# CONFIGURACIONES ADICIONALES
# ============================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
