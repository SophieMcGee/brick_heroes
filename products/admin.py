from django.contrib import admin
from .models import Category, Product, Review


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('friendly_name', 'name')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'category', 'get_average_rating', 'image', 'is_borrowed')

    def get_average_rating(self, obj):
        return obj.average_rating

    get_average_rating.admin_order_field = 'rating' 
    get_average_rating.short_description = 'Avg. Rating'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review)