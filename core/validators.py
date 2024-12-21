from django.core.exceptions import ValidationError
import re


def validate_password(password):
    """
    Проверяет что пароль не менее 8 знаков и содержит цифру
    """
    if len(password) < 8:
        raise ValidationError("Пароль должен быть не менее 8 символов")
    if not re.search(r'\d', password):
        raise ValidationError("Пароль должен содержать хотя бы одну цифру")


def validate_email_domain(email):
    """
    Проверяет что домен входит в число разрешенных
    """
    allowed_domains = ["mail.ru", "yandex.ru"]
    domain = email.split("@")[-1]
    if domain not in allowed_domains:
        raise ValidationError(f"Домен должен быть из списка разрешенных: {', '.join(allowed_domains)}.")