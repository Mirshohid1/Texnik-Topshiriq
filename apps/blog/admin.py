from django.contrib import admin
from .models import BlogPost


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at', 'is_published')
    list_filter = ('is_published', 'author')
    search_fields = ('title', 'content', 'author__username')
    ordering = ('-created_at',)
    list_editable = ('is_published',)
    date_hierarchy = 'created_at'

    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'author', 'is_published')
        }),
        ('Date Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['publish_selected', 'unpublish_selected']

    def publish_selected(self, request, queryset):
        queryset.update(is_published=True)
    publish_selected.short_description = "Publish selected entries"

    def unpublish_selected(self, request, queryset):
        queryset.update(is_published=False)
    unpublish_selected.short_description = "Unpublish selected entries"


admin.site.register(BlogPost, BlogPostAdmin)
