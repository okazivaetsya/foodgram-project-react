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


admin.site.register(FoodgramUser, UserAdmin)
