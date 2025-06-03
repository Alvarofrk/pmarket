from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from .models import CustomUser


class CustomRegisterSerializer(RegisterSerializer):
    def __init__(self, *args, **kwargs):
        print("INSTANCIANDO CustomRegisterSerializer")
        super().__init__(*args, **kwargs)
    username = serializers.CharField(required=True, max_length=150)
    name = serializers.CharField(required=True, max_length=150)
    phone = serializers.CharField(required=False, max_length=15)

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()
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

class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email', 'username', 'name', 'phone')
