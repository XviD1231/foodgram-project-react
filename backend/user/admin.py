from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff',
                    'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email')


admin.site.register(User, CustomUserAdmin)
