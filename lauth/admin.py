from django.contrib import admin
from .models import VerificationCode


@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ['email', 'code', 'created_at', 'is_used']
    list_filter = ['is_used', 'created_at']
    search_fields = ['email', 'code']
    readonly_fields = ['created_at']
