# 🔐 Configuración de Password Reset - Perú Ofertas

## 📋 Resumen de la Implementación

Se ha implementado un sistema completo de restablecimiento de contraseñas usando **dj-rest-auth** y **Django Allauth** con las siguientes características:

- ✅ Solicitud de password reset por email
- ✅ Validación de email existente
- ✅ Envío de email con enlace seguro
- ✅ Confirmación de password reset con token
- ✅ Validaciones de seguridad de contraseña
- ✅ Expiración automática de enlaces (24 horas)
- ✅ Templates de email personalizados
- ✅ Frontend React Native completo

---

## 🚀 Pasos para Activar el Sistema

### 1️⃣ Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto `pmarket/`:

```bash
# Configuración de Email SMTP
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
DEFAULT_FROM_EMAIL=Perú Ofertas <noreply@peruofertas.com>

# Configuración de Password Reset
PASSWORD_RESET_TIMEOUT=86400
```

### 2️⃣ Configurar Gmail (Recomendado)

#### Para Gmail, necesitas generar una "App Password":

1. Ve a [Google Account Settings](https://myaccount.google.com/)
2. Selecciona "Security" → "2-Step Verification"
3. En la parte inferior, selecciona "App passwords"
4. Genera una nueva app password para "Mail"
5. Usa esa contraseña en `EMAIL_HOST_PASSWORD`

#### ⚠️ IMPORTANTE:
- **NO uses tu contraseña normal de Gmail**
- **Solo usa App Passwords generadas específicamente**
- **Habilita 2FA en tu cuenta de Google**

### 3️⃣ Alternativas de Email

#### SendGrid:
```bash
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=tu-sendgrid-api-key
```

#### Mailgun:
```bash
EMAIL_HOST=smtp.mailgun.org
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-username
EMAIL_HOST_PASSWORD=tu-mailgun-password
```

---

## 🔧 Endpoints de la API

### Password Reset Request
```
POST /auth/password/reset/
Content-Type: application/json

{
  "email": "usuario@ejemplo.com"
}
```

### Password Reset Confirm
```
POST /auth/password/reset/confirm/
Content-Type: application/json

{
  "uid": "user_id_from_email",
  "token": "token_from_email",
  "new_password1": "nueva_contraseña123",
  "new_password2": "nueva_contraseña123"
}
```

---

## 📱 Pantallas del Frontend

### 1. **ForgotPasswordScreen**
- Pantalla para solicitar password reset
- Validación de email existente
- Confirmación de envío

### 2. **ResetPasswordScreen**
- Pantalla para establecer nueva contraseña
- Validaciones de seguridad
- Confirmación de cambio exitoso

### 3. **Integración en LoginScreen**
- Botón "¿Olvidaste tu contraseña?" agregado
- Navegación a pantalla de password reset

---

## 🎨 Templates de Email

### Ubicación:
```
pmarket/drfarequipamarket/users/templates/account/email/
├── password_reset_key_message_subject.txt
├── password_reset_key_message.txt
└── password_reset_key_message.html
```

### Personalización:
- Colores de marca (rojo #E80B02)
- Logo y branding de Perú Ofertas
- Mensajes en español
- Diseño responsive para email

---

## 🔒 Características de Seguridad

### Validaciones de Contraseña:
- ✅ Mínimo 8 caracteres
- ✅ Al menos una letra
- ✅ Al menos un número
- ✅ Caracteres especiales permitidos

### Seguridad del Sistema:
- ✅ Tokens únicos por solicitud
- ✅ Expiración automática (24 horas)
- ✅ Validación de UID y token
- ✅ Rate limiting implícito
- ✅ No revela información de usuarios existentes

---

## 🧪 Testing

### 1. **Desarrollo (Console Backend)**
```bash
# Los emails se mostrarán en la consola del servidor
python manage.py runserver
```

### 2. **Producción (SMTP Real)**
```bash
# Configura las variables de entorno y reinicia el servidor
# Los emails se enviarán por SMTP real
```

---

## 🚨 Solución de Problemas

### Error: "SMTP Authentication failed"
- Verifica que `EMAIL_HOST_PASSWORD` sea una App Password válida
- Asegúrate de que 2FA esté habilitado en tu cuenta de Google

### Error: "Connection refused"
- Verifica que `EMAIL_HOST` y `EMAIL_PORT` sean correctos
- Asegúrate de que tu proveedor de email permita conexiones SMTP

### Emails no se envían
- Revisa los logs del servidor Django
- Verifica la configuración de `EMAIL_BACKEND`
- Confirma que las variables de entorno estén cargadas

---

## 📚 Recursos Adicionales

- [Django Email Documentation](https://docs.djangoproject.com/en/5.1/topics/email/)
- [dj-rest-auth Password Reset](https://dj-rest-auth.readthedocs.io/en/latest/api_endpoints.html#password-reset)
- [Django Allauth Documentation](https://django-allauth.readthedocs.io/en/latest/)
- [Gmail App Passwords](https://support.google.com/accounts/answer/185833)

---

## ✅ Checklist de Verificación

- [ ] Variables de entorno configuradas
- [ ] App Password generada (Gmail)
- [ ] Servidor reiniciado
- [ ] Frontend integrado
- [ ] Navegación funcionando
- [ ] Emails enviándose correctamente
- [ ] Password reset funcionando end-to-end

---

**🎉 ¡Tu sistema de password reset está listo para usar!**
