from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from typing import Optional
from .models import Category, Product, ProductImage, District, Message, Chat


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):
    url = serializers.ImageField(use_url=True)

    class Meta:
        model = ProductImage
        fields = ("url",)

    def create(self, validated_data):
        # Generar nombre y texto alternativo automáticamente
        validated_data['name'] = f"Product Image {validated_data.get('product').id}"
        validated_data['alternative_text'] = f"Image for product {validated_data.get('product').id}"
        return super().create(validated_data)


class ProductSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True, required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=True)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    price = serializers.IntegerField(required=True)
    state = serializers.CharField(required=True)
    district = serializers.CharField(required=True)
    currency = serializers.CharField(required=True)
    vendor_id = serializers.SerializerMethodField()
    vendor_username = serializers.SerializerMethodField()

    class Meta:
        model = Product
        exclude = ("vendor",)

    @extend_schema_field(serializers.IntegerField(allow_null=True))
    def get_vendor_id(self, obj: Product) -> Optional[int]:
        return obj.vendor.id if obj.vendor else None

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_vendor_username(self, obj: Product) -> Optional[str]:
        return obj.vendor.username if obj.vendor else None

    def create(self, validated_data):
        request = self.context.get('request')
        product_images_files = request.FILES.getlist('product_image') if request else []
        product = Product.objects.create(**validated_data)
        for image_file in product_images_files:
            ProductImage.objects.create(product=product, url=image_file)
        return product


# Serializer para District
class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = "__all__"


# Serializers para Chat y Message
class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    class Meta:
        model = Message
        fields = ['id', 'chat', 'sender', 'sender_username', 'text', 'created_at']

class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    buyer_username = serializers.CharField(source='buyer.username', read_only=True)
    vendor_username = serializers.CharField(source='vendor.username', read_only=True)
    class Meta:
        model = Chat
        fields = ['id', 'product', 'buyer', 'vendor', 'buyer_username', 'vendor_username', 'created_at', 'messages']
