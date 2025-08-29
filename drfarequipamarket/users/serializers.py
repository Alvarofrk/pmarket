from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from dj_rest_auth.serializers import PasswordResetSerializer, PasswordResetConfirmSerializer
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'name', 'phone')
        read_only_fields = ('email',)

class CustomRegisterSerializer(RegisterSerializer):
    def __init__(self, *args, **kwargs):
        print("INSTANCIANDO CustomRegisterSerializer")
        super().__init__(*args, **kwargs)
    username = serializers.CharField(required=True, max_length=150)
    name = serializers.CharField(required=True, max_length=150)
    phone = serializers.CharField(required=False, max_length=15)

    def get_cleaned_data(self):
        return {
            "username": self.validated_data.get("username", ""),
            "password1": self.validated_data.get("password1", ""),
            "password2": self.validated_data.get("password2", ""),
            "email": self.validated_data.get("email", ""),
            "name": self.validated_data.get("name", ""),
            "phone": self.validated_data.get("phone", ""),
        }

    def validate(self, data):
        print(f"DATA RECIBIDA EN REGISTRO: {data}")
        return super().validate(data)
    
    def save(self, request):
        user = super().save(request)
        user.name = self.cleaned_data.get('name', '')
        user.phone = self.cleaned_data.get('phone', '')
        user.save()
        return user

class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email', 'username', 'name', 'phone')

# Serializers para Password Reset
class CustomPasswordResetSerializer(PasswordResetSerializer):
    password_reset_form_class = PasswordResetForm
    
    def get_email_options(self):
        return {
            'email_template_name': 'account/email/password_reset_key_message.txt',
            'subject_template_name': 'account/email/password_reset_key_message_subject.txt',
            'html_email_template_name': 'account/email/password_reset_key_message.html',
            'extra_email_context': {
                'site_name': 'Perú Ofertas',
                'user': self.user,
            }
        }

class CustomPasswordResetConfirmSerializer(PasswordResetConfirmSerializer):
    set_password_form_class = SetPasswordForm
