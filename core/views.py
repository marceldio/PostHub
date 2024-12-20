from rest_framework.viewsets import ModelViewSet
from .models import CustomUser, Post, Comment
from .serializers import CustomUserSerializer, PostSerializer, CommentSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from .permissions import IsAuthorOrReadOnly, IsAdminOrAuthor


class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_update(self, serializer):
        # Проверяем, что пользователь редактирует только себя
        if self.request.user != self.get_object():
            self.permission_denied(self.request, message="You can only edit your own profile.")
        serializer.save()


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_destroy(self, instance):
        # Проверяем, что пользователь автор или администратор
        if not self.request.user.is_staff and instance.author != self.request.user:
            self.permission_denied(self.request, message="You can only delete your own posts.")
        instance.delete()


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminOrAuthor]

    def perform_destroy(self, instance):
        # Проверяем, что пользователь автор или администратор
        if not self.request.user.is_staff and instance.author != self.request.user:
            self.permission_denied(self.request, message="You can only delete your own comments.")
        instance.delete()
