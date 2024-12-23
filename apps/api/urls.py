from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from . import views


router = DefaultRouter()
router.register(r'posts', views.BlogPostViewSet)
router.register(r'comments', views.CommentViewSet)

urlpatterns = [
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair_login'),
    path('auth/logout/', views.CustomLogoutView.as_view(), name='token_blacklist_logout'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls