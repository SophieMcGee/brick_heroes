from django.contrib import admin
from .models import Product, Category, Review, Rating

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

class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "rating", "is_approved", "created_on")
    list_filter = ("is_approved",)
    actions = ["approve_reviews"]
    ordering = ["is_approved", "-created_on"]  # Shows unapproved reviews first

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Selected reviews approved.")
    approve_reviews.short_description = "Approve selected reviews"

admin.site.register(Review, ReviewAdmin)
admin.site.register(Rating)
