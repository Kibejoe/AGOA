from django.contrib import admin
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['firstname', 'lastname', 'email', 'is_active', 'is_superuser']
    readonly_fields = ['password', 'firstname', 'lastname', 'email', 'phone']
admin.site.register(CustomUser, CustomUserAdmin)