from .base import *
from google.oauth2 import service_account

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR  / "db.sqlite3",
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE', default='django.db.backends.postgresql'),
        'NAME': config('DB_NAME', default='arequipamarket'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432', cast=int),
        'CONN_MAX_AGE': 0,
        'OPTIONS': {
            'connect_timeout': 10,
        }
    }
}

ALLOWED_HOSTS = [
    "*",
]

CSRF_TRUSTED_ORIGINS = [
    "https://aqp-marketplace-api-dev-312428306361.southamerica-east1.run.app",
    "http://*",
    "https://*",
]

# Configuración de almacenamiento local
#STATIC_URL = '/static/'
#STATIC_ROOT = BASE_DIR / 'staticfiles'
#MEDIA_URL = '/media/'
#MEDIA_ROOT = BASE_DIR / 'media'

# Eliminar la configuración de Google Cloud Storage
# STORAGES = {
#     "default": {
#         "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
#         "OPTIONS": {
#             "bucket_name": "arequipamarket",
#             "project_id": "arequipamarketplace",
#             "credentials": service_account.Credentials.from_service_account_file(
#                 "drfarequipamarket/credentials/arequipamarketplace-1998beab8d2e.json"
#             ),
#             "file_overwrite": False,
#         },
#     },
#     "staticfiles": {
#         "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
#         "OPTIONS": {
#             "bucket_name": "arequipamarket",
#             "project_id": "arequipamarketplace",
#             "credentials": service_account.Credentials.from_service_account_file(
#                 "drfarequipamarket/credentials/arequipamarketplace-1998beab8d2e.json"
#             ),
#         },
#     },
# }
