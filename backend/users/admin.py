from django.contrib import admin
from django.contrib.auth import admin as upstream
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(upstream.UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email', 'public_key')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
