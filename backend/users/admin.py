from django.contrib import admin
from recipes.models import User


class UserAdmin(admin.ModelAdmin):
    """Административная модель пользователя."""
    list_display = (
        'username', 'email',
        'first_name', 'last_name',
        'is_staff', 'is_active',
        'last_login', 'date_joined'
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('first_name', 'last_name', 'email', 'is_active', 'is_staff')
    empty_value_display = '-empty-'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
