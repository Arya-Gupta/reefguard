"""
Admin configuration for ReefGuard models.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Reef, Event, Article, ImageGallery, ReefBookmark


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin interface for CustomUser model."""
    list_display = ['username', 'email', 'role', 'first_name', 'last_name', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']

    fieldsets = UserAdmin.fieldsets + (
        ('ReefGuard Info', {'fields': ('role', 'bio', 'organization')}),
    )


@admin.register(Reef)
class ReefAdmin(admin.ModelAdmin):
    """Admin interface for Reef model."""
    list_display = ['name', 'region', 'country', 'health_status', 'created_at']
    list_filter = ['region', 'health_status']
    search_fields = ['name', 'country', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Admin interface for Event model."""
    list_display = ['title', 'reef', 'event_type', 'severity', 'event_date', 'resolved']
    list_filter = ['event_type', 'severity', 'resolved', 'event_date']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'event_date'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Admin interface for Article model."""
    list_display = ['title', 'category', 'author', 'published', 'featured', 'created_at']
    list_filter = ['category', 'published', 'featured']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ImageGallery)
class ImageGalleryAdmin(admin.ModelAdmin):
    """Admin interface for ImageGallery model."""
    list_display = ['title', 'media_type', 'reef', 'event', 'uploaded_by', 'uploaded_at']
    list_filter = ['media_type', 'uploaded_at']
    search_fields = ['title', 'description']
    readonly_fields = ['uploaded_at']


@admin.register(ReefBookmark)
class ReefBookmarkAdmin(admin.ModelAdmin):
    """Admin interface for ReefBookmark model."""
    list_display = ['user', 'reef', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'reef__name', 'notes']
    readonly_fields = ['created_at']
