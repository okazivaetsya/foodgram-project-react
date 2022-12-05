from django.contrib.auth.base_user import BaseUserManager


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
        if not email:
            raise ValueError('Поле Email является обязательным')
        if not username:
            raise ValueError('Поле username является обязательным')
        if not first_name:
            raise ValueError('Поле first_name является обязательным')
        if not last_name:
            raise ValueError('Поле last_name является обязательным')
        if not password:
            raise ValueError('Поле password является обязательным')
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

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(
            email, username,
            first_name, last_name,
            password, **extra_fields
        )
