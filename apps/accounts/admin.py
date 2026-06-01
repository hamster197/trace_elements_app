from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

# Register your models here.


@admin.register(get_user_model())
class ProjectUserModelAdmin(UserAdmin):
    list_display=('pk', 'email', 'last_name', 'first_name',)
    fieldsets = (
        ('Fields for all users', {
            'fields': (
                'email', 'password', 'last_name', 'first_name', 'patronymic', 'phone', 'male', 'female', 'date_of_birth',
                'is_active', 'is_staff', 'is_superuser', 'groups', )
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2', 'last_name', 'first_name', 'patronymic', 'phone',
                       'male', 'female', 'date_of_birth', 'is_active', 'is_staff', 'is_superuser', 'groups',),
        }),
    )
    ordering = ('pk',)
