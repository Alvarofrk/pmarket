from django.db import models
from django.conf import settings
from drfarequipamarket.users import models as UserModels
from drfarequipamarket.users.models import CustomUser
from drfarequipamarket.product import models as ProductModels
from storages.backends.s3boto3 import S3Boto3Storage


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.id) + " - " + self.name


class Departamento(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Province(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    # Constants
    PRODUCT_STATE = [
        ("NEW", "Nuevo - nunca usado"),
        ("USED/A", "Usado - como nuevo"),
        ("USED/B", "Usado - bueno"),
        ("USED/C", "Usado - bastante"),
    ]

    CURRENCIES = [("USD", "Dólares"), ("PEN", "Soles")]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    currency = models.CharField(
        max_length=3, default="USD", choices=CURRENCIES
    )
    state = models.CharField(max_length=6, choices=PRODUCT_STATE)
    is_available = models.BooleanField(default=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    vendor = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)

    # NUEVOS CAMPOS
    departamento = models.CharField(max_length=100, blank=True, null=True)
    provincia = models.CharField(max_length=100, blank=True, null=True)
    distrito = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.id) + " - " + self.name


class ProductImage(models.Model):
    name = models.CharField(max_length=100, blank=True)
    alternative_text = models.CharField(max_length=100, blank=True)
    url = models.ImageField(upload_to='product_images/', storage=S3Boto3Storage())
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_image"
    )

    def __str__(self):
        return self.name or f"Image for product {self.product.id}"


# MODELOS DE CHAT
class Chat(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='chats')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chats_as_buyer')
    vendor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chats_as_vendor')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat producto {self.product.id} - comprador {self.buyer.id} - vendedor {self.vendor.id}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensaje de {self.sender} en chat {self.chat.id} ({self.created_at})"
