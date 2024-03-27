from django.contrib import admin

from .models import CustomUser, Token

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'username']
    # list_editable = ['email']
    list_filter = ['email']

class TokenAdmin(admin.ModelAdmin):
    list_display = ['id', 'token', 'user']
    list_filter = ['user', 'created_at', 'expire']

admin.site.register(Token, TokenAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
