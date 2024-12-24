from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny, BasePermission
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView

from ..blog.models import BlogPost, Comment
from ..blog.serializers import (
    BlogPostSerializer, BlogPostInputSerializer,
    CommentSerializer, CommentInputSerializer,
)
from ..users.models import User
from ..users.serializers import RegisterSerializer, ProfileSerializer, CustomTokenObtainPairSerializer
from ..users.permissions import IsProfileOwnerOrAdmin


class BaseViewSet(ModelViewSet):
    """
    A base view set that provides common functionality for handling
    model instances in a DRF viewset. This includes dynamic selection
    of serializers, permission checks for create, update, and destroy
    actions, and saving the current user as the author for created instances.
    """

    serializer_class = None
    input_serializer_class = None
    is_comment: bool = False

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the current action
        (create, update, partial_update, or other actions).
        """
        if self.action in ['create', 'update', 'partial_update']:
            return self.input_serializer_class
        return self.serializer_class

    def perform_create(self, serializer):
        """
        Saves the instance, setting the current user as the author.
        """
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """
        Updates the instance after verifying the user's permission to edit it.
        Raises PermissionDenied if the user lacks permission.
        """
        comment = self.get_object()
        if not self._my_permission(comment):
            raise PermissionDenied("You don't have permission to edit this object.")
        serializer.save()

    def perform_destroy(self, instance):
        """
        Deletes the instance after verifying the user's permission to delete it.
        Raises PermissionDenied if the user lacks permission.
        """
        if not self._my_permission(instance):
            raise PermissionDenied("You don't have permission to delete this object.")
        super().perform_destroy(instance)

    def _my_permission(self, obj):
        """
        Checks if the current user has permission to perform the action on the given object.
        Permissions differ based on whether the object is a comment or not.
        """
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
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = BlogPostSerializer
    input_serializer_class = BlogPostInputSerializer


class CommentViewSet(BaseViewSet):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    input_serializer_class = CommentInputSerializer
    is_comment = True


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi",
                'user_id': user.id,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer


class CustomLogoutView(TokenBlacklistView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 205:
            return Response({'message': "Tizimdan muvaffaqiyatli chiqdingiz"}, status.HTTP_200_OK)
        return response


class ProfileView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            self.permission_classes = [IsAuthenticated, IsProfileOwnerOrAdmin]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return super().get_permissions()

    def is_profile_owner_or_admin(self, request, view):
        profile = self.get_object()
        return profile.user == request.user or self.request.user.role == 'admin'
