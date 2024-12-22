from django.contrib import admin
from django.utils import timezone
from .models import BlogPost, Comment


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at', 'is_published')
    list_filter = ('is_published', 'author')
    search_fields = ('title', 'content', 'author__username')
    ordering = ('-created_at',)
    list_editable = ('is_published',)
    date_hierarchy = 'created_at'

    # Просто исключим created_at и updated_at из формы
    exclude = ('created_at', 'updated_at')  # Эти поля не редактируются

    actions = ['publish_selected', 'unpublish_selected']

    def publish_selected(self, request, queryset):
        queryset.update(is_published=True)
    publish_selected.short_description = "Publish selected entries"

    def unpublish_selected(self, request, queryset):
        queryset.update(is_published=False)
    unpublish_selected.short_description = "Unpublish selected entries"


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'content', 'created_at', 'updated_at')
    list_filter = ('post', 'author')
    search_fields = ('content', 'author__username', 'post__title')
    ordering = ('-created_at',)

    # При сохранении, автоматически заполняем created_at и updated_at
    def save_model(self, request, obj, form, change):
        if not obj.id:  # Если это новый объект, устанавливаем created_at
            obj.created_at = timezone.now()
        obj.updated_at = timezone.now()  # Обновляем updated_at
        super().save_model(request, obj, form, change)


admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Comment, CommentAdmin)
