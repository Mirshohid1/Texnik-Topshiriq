from rest_framework import serializers
from .models import BlogPost
from ..users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class BlogPostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

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
