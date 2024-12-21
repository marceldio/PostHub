from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_password, validate_email_domain


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Применяем валидатор для email
    email = models.EmailField(validators=[validate_email_domain], unique=True)

    def set_password(self, raw_password):
        # Применяем валидатор для пароля перед сохранением
        validate_password(raw_password)
        super().set_password(raw_password)


    def __str__(self):
        return self.username


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"
