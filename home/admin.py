from django.contrib import admin
from .models import LegoSet, ContactMessage, Borrowing

@admin.register(LegoSet)
class LegoSetAdmin(admin.ModelAdmin):
    list_display = ('title', 'piece_count', 'availability', 'theme')
    search_fields = ('title', 'theme')
    list_filter = ('availability', 'theme')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email', 'message')
    list_filter = ('created_at',)

@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('user', 'lego_set', 'due_date', 'is_returned')
    search_fields = ('user__username', 'lego_set')
    list_filter = ('is_returned', 'due_date')
