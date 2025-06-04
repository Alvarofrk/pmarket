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
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='provinces')
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('departamento', 'name') # Ensure province names are unique per departamento

    def __str__(self):
        return f"{self.name}, {self.departamento.name}"


class District(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='districts', null=True, blank=True) # Null/blank true temporarily if you have existing districts
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('province', 'name') # Ensure district names are unique per province

    def __str__(self):
        return f"{self.name}, {self.province.name}"


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
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='products_in_departamento', null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='products_in_province', null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='products_in_district', null=True, blank=True)
    is_available = models.BooleanField(default=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    vendor = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)

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
