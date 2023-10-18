from django.contrib import admin
from .models import *


class InlineKeys(admin.StackedInline):
    model = RecipientKeys


@admin.register(Secret)
class SecretAdmin(admin.ModelAdmin):
    inlines = [InlineKeys]
    readonly_fields = ("key",)

# @admin.register(Shared_Secret)
# class SecretAdmin(admin.ModelAdmin):
#     pass


@admin.register(RecipientKeys)
class SecretAdmin(admin.ModelAdmin):
    pass
