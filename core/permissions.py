from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    """
    Разрешает доступ на редактирование только автору объекта.
    Доступ на чтение разрешен всем.
    """

    def has_object_permission(self, request, view, obj):
        # Если запрос на чтение (GET, HEAD, OPTIONS), то разрешить
        if request.method in SAFE_METHODS:
            return True
        # Разрешить только если пользователь — автор объекта
        return obj.author == request.user


class IsAdminOrAuthor(BasePermission):
    """
    Разрешает удалять объект только администратору или автору.
    """

    def has_object_permission(self, request, view, obj):
        # Администратор может всё
        if request.user.is_staff:
            return True
        # Автор может удалять свои объекты
        return obj.author == request.user