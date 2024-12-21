from rest_framework import serializers
from .models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = (
            'id',
            'title', 'content', 'author',
            'created_at', 'updated_at', 'is_published',
        )


class BlogPostInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ('title', 'content', 'is_published')
