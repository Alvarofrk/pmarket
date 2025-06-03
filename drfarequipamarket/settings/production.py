from .base import *
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
from decouple import config

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG se puede configurar mediante variable de entorno
DEBUG = config('DEBUG', default=True, cast=bool)

# Configuración de hosts permitidos
ALLOWED_HOSTS = [
    "pmarket.onrender.com",
    "*.onrender.com",
    "localhost",
    "127.0.0.1",
]

# Asegurarse de que las aplicaciones de Django estén correctamente configuradas
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

THIRD_PARTY_APPS = [
    'cloudinary_storage',  # Debe ir antes de staticfiles
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_auth',
    'rest_auth.registration',
]

LOCAL_APPS = [
    'drfarequipamarket.users.apps.UsersConfig',
    'drfarequipamarket.product.apps.ProductConfig',
    'drfarequipamarket.chat.apps.ChatConfig',
]

INSTALLED_APPS = ['daphne'] + DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Configuración de base de datos para producción
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config('DB_NAME', default='arequipamarket'),
        "USER": config('DB_USER', default='postgres'),
        "PASSWORD": config('DB_PASSWORD', default=''),
        "HOST": config('DB_HOST', default='localhost'),
        "PORT": config('DB_PORT', default='5432'),
        "CONN_MAX_AGE": 60,  # Mantener conexiones vivas por 60 segundos
        "OPTIONS": {
            "connect_timeout": 10,
        }
    }
}

# Configuración de Cloudinary
CLOUDINARY = {
    'cloud_name': config('CLOUDINARY_CLOUD_NAME'),
    'api_key': config('CLOUDINARY_API_KEY'),
    'api_secret': config('CLOUDINARY_API_SECRET'),
    'secure': True,  # Forzar HTTPS
}

# Configuración de archivos estáticos y media
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configurar Cloudinary como backend de almacenamiento
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'

# Configuración de seguridad
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000  # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# CORS configuration
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    'https://pmarket.onrender.com',
    'https://*.onrender.com',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]
CORS_ALLOWED_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ALLOWED_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# CSRF configuration
CSRF_TRUSTED_ORIGINS = [
    'https://pmarket.onrender.com',
    'https://*.onrender.com',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_USE_SESSIONS = True

# Session configuration
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_AGE = 1209600  # 2 semanas en segundos

# Email configuration (usando console backend para desarrollo)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'django': {
        'handlers': ['console'],
        'level': 'INFO',
        'propagate': False,
    },
}
