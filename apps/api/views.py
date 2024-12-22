from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet
from ..blog.models import BlogPost, Comment
from ..blog.serializers import (
    BlogPostSerializer, BlogPostInputSerializer,
    CommentSerializer, CommentInputSerializer,
)


class BlogPostViewSet(ModelViewSet):
    queryset = BlogPost.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BlogPostInputSerializer
        return BlogPostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        post = self.get_object()
        if self.request.user != post.author:
            raise PermissionDenied("You can only edit your posts.")
        serializer.save()

    def perform_destroy(self, instance):
        post = self.get_object()
        if post.author != self.request.user:
            raise PermissionDenied("You can only delete your posts.")
        instance.delete()


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CommentInputSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        comment = self.get_object()
        if comment.author != self.request.user:
            raise PermissionDenied("You can only edit your comments or comments your posts.")
        serializer.save()

    def perform_destroy(self, instance):
        comment = self.get_object()
        if comment.author != self.request.user:
            raise PermissionDenied("You can only delete your comments or comments your posts.")
        instance.delete()
