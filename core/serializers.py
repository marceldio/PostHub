from rest_framework import serializers
from .models import CustomUser, Post, Comment
from .validators import validate_password, validate_email_domain


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) # Скрываем пароль в выводе

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'phone', 'birth_date', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_password(self, value):
        """
        Вызываем кастомный валидатор для пароля.
        """
        validate_password(value)
        return value

    def validate_email_domain(self, value):
        """
        Вызываем кастомный валидатор для email.
        """
        validate_email_domain(value)
        return value

    def create(self, validated_data):
        """
        Создаем пользователя с хэшированным паролем.
        """
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)  # Используем метод модели для установки пароля
        user.save()
        return user


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'content', 'created_at', 'updated_at']


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)  # поле комментариев

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'image', 'author', 'comments', 'created_at', 'updated_at']
