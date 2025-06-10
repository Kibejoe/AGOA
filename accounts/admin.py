from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.html import format_html


CustomUser = get_user_model()

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['firstname', 'lastname', 'email', 'is_active', 'is_superuser']
    readonly_fields = ['password', 'firstname', 'lastname', 'email', 'phone', 'id_file']




admin.site.register(CustomUser, CustomUserAdmin)