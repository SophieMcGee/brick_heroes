from django.contrib import admin
from .models import Category, Product

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('friendly_name', 'name')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'category', 'rating', 'image', 'is_borrowed')
    ordering = ('sku',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)