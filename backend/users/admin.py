from django.contrib import admin
from .models import FoodgramUser, Follow


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'username',
        'first_name',
        'last_name',
        'password'
    )
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    list_filter = ('user', 'author')
    empty_value_display = '-пусто-'


admin.site.register(FoodgramUser, UserAdmin)
admin.site.register(Follow, FollowAdmin)
