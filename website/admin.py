from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'source_page', 'submitted_at')
    list_filter = ('source_page', 'submitted_at')
    search_fields = ('name', 'email', 'phone', 'message')
