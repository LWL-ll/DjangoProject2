from django.contrib import admin
from .models import UserPreference


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'taste', 'cuisine', 'budget', 'allergy', 'created_at', 'updated_at']
    list_filter = ['taste', 'cuisine', 'budget', 'created_at']
    search_fields = ['user__username', 'taste', 'cuisine', 'allergy', 'demand']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20
