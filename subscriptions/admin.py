from django.contrib import admin
from .models import SubscriptionPlan, Subscription, Borrowing, UserProfile

# Inline class for Borrowing management in Subscription view
class BorrowingInline(admin.TabularInline):
    model = Borrowing
    extra = 1  # Adds one extra row for new borrowing records

# Admin for SubscriptionPlan
@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'max_active_borrows', 'stripe_price_id')
    search_fields = ('name', 'stripe_price_id')
    list_filter = ('max_active_borrows',)

# Admin for Subscription
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription_plan', 'start_date', 'end_date', 'status')
    search_fields = ('user__username', 'user__email', 'subscription_plan__name')
    list_filter = ('status', 'subscription_plan__name')
    inlines = [BorrowingInline]  # Allows managing borrowings from the subscription form

# Admin for Borrowing
@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('user', 'lego_set', 'borrowed_on', 'returned_on', 'is_returned')
    search_fields = ('user__username', 'lego_set__name')
    list_filter = ('is_returned', 'borrowed_on')

# Admin for UserProfile
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription', 'borrowed_this_month')
    search_fields = ('user__username', 'user__email')
    list_filter = ('subscription__subscription_plan__name',)
