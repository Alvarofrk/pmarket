"""
Configuración de email para el proyecto Perú Ofertas
"""
from decouple import config

# Configuración base de email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=False, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='noreply@peruofertas.com')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='Perú Ofertas <noreply@peruofertas.com>')

# Configuración de password reset
PASSWORD_RESET_TIMEOUT = config('PASSWORD_RESET_TIMEOUT', default=86400, cast=int)  # 24 horas

# Configuración para desarrollo (fallback a console si no hay credenciales)
if not EMAIL_HOST_PASSWORD:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    print("⚠️  EMAIL_HOST_PASSWORD no configurado. Usando backend de consola para desarrollo.")
    print("📧 Para usar email real, configura EMAIL_HOST_PASSWORD en tu archivo .env")
else:
    print("✅ Configuración de email SMTP activada")
