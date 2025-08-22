from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'name', 'phone')
        read_only_fields = ('email',)

class CustomRegisterSerializer(RegisterSerializer):
    def __init__(self, *args, **kwargs):
        print("=== CONSTRUCTOR DEL SERIALIZER ===")
        print("ARGS:", args)
        print("KWARGS:", kwargs)
        print("INSTANCIANDO CustomRegisterSerializer")
        super().__init__(*args, **kwargs)
        print("=== FIN DEL CONSTRUCTOR ===")

    username = serializers.CharField(required=True, max_length=150)
    name = serializers.CharField(required=True, max_length=150)
    phone = serializers.CharField(required=False, max_length=15)

    def get_cleaned_data(self):
        print("=== GET_CLEANED_DATA ===")
        cleaned_data = super(CustomRegisterSerializer, self).get_cleaned_data()
        print("CLEANED_DATA DEL PADRE:", cleaned_data)
        result = {
            "username": self.validated_data.get("username", ""),
            "password1": self.validated_data.get("password1", ""),
            "password2": self.validated_data.get("password2", ""),
            "email": self.validated_data.get("email", ""),
            "name": self.validated_data.get("name", ""),
            "phone": self.validated_data.get("phone", ""),
        }
        print("CLEANED_DATA FINAL:", result)
        return result

    def validate(self, data):
        print("=== VALIDATE ===")
        print("DATA RECIBIDA EN REGISTRO:", data)
        print("VALIDATED_DATA ANTES:", self.validated_data)
        result = super().validate(data)
        print("VALIDATED_DATA DESPUÉS:", self.validated_data)
        print("RESULTADO VALIDATE:", result)
        return result

    def save(self, request):
        print("=== INICIO DEL PROCESO DE REGISTRO ===")
        print("INSTANCIANDO CustomRegisterSerializer")
        print("REQUEST:", request)
        print("VALIDATED_DATA:", self.validated_data)

        try:
            print("LLAMANDO AL MÉTODO SAVE DEL PADRE...")
            user = super(CustomRegisterSerializer, self).save(request)
            print("USUARIO CREADO EXITOSAMENTE:", user)
            print("ID DEL USUARIO:", user.id)
            print("EMAIL DEL USUARIO:", user.email)
            print("=== FIN DEL PROCESO DE REGISTRO ===")
            return user
        except Exception as e:
            print("ERROR AL CREAR USUARIO:", str(e))
            print("TIPO DE ERROR:", type(e).__name__)
            print("TRACEBACK:", e.__traceback__)
            raise e

class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email', 'username', 'name', 'phone')
