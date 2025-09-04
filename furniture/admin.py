from django.contrib import admin
from .models import Product, ProductImage, Category

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # number of extra empty forms

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",) 