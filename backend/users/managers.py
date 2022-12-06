from django.contrib.auth.base_user import BaseUserManager
from .services import check_empty_fields


class CustomUserManager(BaseUserManager):
    """
    Кастомный менеджер модели юзер, где основным полем являтся email.
    """
    def create_user(
        self, email, username,
        first_name, last_name,
        password, **extra_fields
    ):
        """
        Создаем и сохраняем пользователя с обязательными полями:
        email, username, first_name, last_name, password.
        """
        check_empty_fields(email, username, first_name, last_name, password)
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self, email, username,
        first_name, last_name,
        password, **extra_fields
    ):
        """
        Создаем суперпользователя (админа).
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(
            email, username,
            first_name, last_name,
            password, **extra_fields
        )
