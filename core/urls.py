from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CustomUserViewSet, PostViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
