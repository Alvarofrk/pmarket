from django.contrib import admin

from .models import Category, Product, ProductImage, District


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    readonly_fields = ('id', )

class DistrictAdmin(admin.ModelAdmin):
    model = District
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(District, DistrictAdmin)