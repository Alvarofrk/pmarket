from rest_framework import serializers
from .models import Category, Product, ProductImage, District


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image']


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
    category_name = serializers.CharField(source='category.name', read_only=True)
    seller_name = serializers.CharField(source='seller.username', read_only=True)
    images = serializers.SerializerMethodField()
    district_name = serializers.CharField(source='district.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'category', 'category_name',
            'seller', 'seller_name', 'images', 'district', 'district_name',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['seller', 'created_at', 'updated_at']

    def get_images(self, obj):
        images = obj.images.all()
        return [{'id': img.id, 'image': img.image.url} for img in images]

    def create(self, validated_data):
        request = self.context.get('request')
        product_images_files = request.FILES.getlist('product_image') if request else []
        product = Product.objects.create(**validated_data)
        for image_file in product_images_files:
            ProductImage.objects.create(product=product, url=image_file)
        return product


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name', 'description']
