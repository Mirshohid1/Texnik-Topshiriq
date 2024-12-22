from rest_framework import serializers
from .models import BlogPost, Comment
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


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'id', 'post', 'author',
            'content', 'created_at', 'updated_at',
        )


class CommentInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('post', 'content')
