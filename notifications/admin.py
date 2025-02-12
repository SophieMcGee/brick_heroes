from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "category", "message", "created_at", "is_read")
    list_filter = ("category", "is_read", "created_at")
    search_fields = ("user__username", "message")
    ordering = ("-created_at",)
