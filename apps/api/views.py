from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet
from ..blog.models import BlogPost, Comment
from ..blog.serializers import (
    BlogPostSerializer, BlogPostInputSerializer,
    CommentSerializer, CommentInputSerializer,
)


class BaseViewSet(ModelViewSet):
    serializer_class = None
    input_serializer_class = None
    is_comment: bool = False

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return self.input_serializer_class
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        comment = self.get_object()
        if not self._my_permission(comment):
            raise PermissionDenied("You don't have permission to edit this object.")
        serializer.save()

    def perform_destroy(self, instance):
        if not self._my_permission(instance):
            raise PermissionDenied("You don't have permission to delete this object.")
        super().perform_destroy(instance)

    def _my_permission(self, obj):
        if self.is_comment:
            return (
                self.request.user == obj.author or
                self.request.user.role == 'admin' or
                self.request.user == obj.post.author
            )
        else:
            return self.request.user == obj.author or self.request.user.role == 'admin'


class BlogPostViewSet(BaseViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    input_serializer_class = BlogPostInputSerializer


class CommentViewSet(BaseViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    input_serializer_class = CommentInputSerializer
    is_comment = True
