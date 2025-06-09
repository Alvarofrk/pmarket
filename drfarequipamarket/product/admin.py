from django.contrib import admin

from .models import Category, Product, ProductImage, District, Departamento, Province


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ('name', 'departamento', 'provincia', 'distrito', 'price', 'category', 'vendor')
    search_fields = ('name', 'departamento', 'provincia', 'distrito', 'category__name', 'vendor__username')
    list_filter = ('departamento', 'provincia', 'distrito', 'category')
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'price', 'currency', 'state', 'is_available', 'category', 'vendor')
        }),
        ('Ubicación', {
            'fields': ('departamento', 'provincia', 'distrito')
        }),
    )


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
admin.site.register(Departamento)
admin.site.register(Province)