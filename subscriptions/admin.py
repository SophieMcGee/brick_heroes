from django.contrib import admin
from .models import Subscription, SubscriptionPlan, UserProfile

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_plan', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'subscription_plan__name')
    search_fields = ('user__username', 'user__email')

    def get_plan(self, obj):
        return obj.subscription_plan.name if obj.subscription_plan else "No Plan"
    get_plan.short_description = 'Plan'

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'max_borrow_per_month', 'max_active_borrows')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription', 'borrowed_this_month')
