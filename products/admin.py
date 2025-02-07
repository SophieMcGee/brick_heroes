from django.contrib import admin
from .models import Product, Category, Review

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1  # Adds one extra empty row for new reviews

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'category', 'rating', 'stock', 'is_borrowed')
    search_fields = ('name', 'description', 'category__name')
    list_filter = ('category', 'is_borrowed')
    inlines = [ReviewInline]  # Allows editing reviews directly within the product form

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'friendly_name')
    search_fields = ('name',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_on')
    list_filter = ('created_on', 'rating')
    search_fields = ('user__username', 'product__name')
