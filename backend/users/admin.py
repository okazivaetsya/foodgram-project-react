from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from recipes.admin import FoodgramAdminModel

from .models import CustomUser, Follow


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Настройка админки для модели кастомного пользователя"""
    model = CustomUser
    list_display = (
        'email', 'username',
        'first_name', 'last_name',
        'is_staff', 'is_active',
    )
    list_filter = ('email', 'is_staff', 'is_active',)
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(Follow)
class FollowAdmin(FoodgramAdminModel):
    """Настройки для модели Подписки"""
    list_display = ('id', 'user', 'author')
    search_fields = ('user', 'author')
    list_filter = ('user', 'author')
