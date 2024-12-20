from rest_framework.viewsets import ModelViewSet
from .models import CustomUser, Post, Comment
from .serializers import CustomUserSerializer, PostSerializer, CommentSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import IsAuthorOrReadOnly, IsAdminOrAuthor


class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        if self.action == 'create':  # Регистрация разрешена всем
            permission_classes = []
        elif self.action in ['list', 'retrieve', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_update(self, serializer):
        if self.request.user != self.get_object():
            self.permission_denied(self.request, message="You can only edit your own profile.")
        serializer.save()


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_destroy(self, instance):
        # print(f"User: {self.request.user}, Staff: {self.request.user.is_staff}, Author: {instance.author}")
        if not self.request.user.is_staff and instance.author != self.request.user:
            # print("Permission denied: not author or staff")
            self.permission_denied(self.request, message="You can only delete your own posts.")
        # print("Post deleted")
        instance.delete()


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrAuthor]

    def perform_destroy(self, instance):
        if not self.request.user.is_staff and instance.author != self.request.user:
            self.permission_denied(self.request, message="You can only delete your own comments.")
        instance.delete()
