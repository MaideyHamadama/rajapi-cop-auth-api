from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields' : ('role', 'profile_picture', 'newsletter_subscription', 'updated_at', 'phone_number', 'is_verified')}),
    )
    list_display = ['username', 'email', 'role', 'is_active', 'newsletter_subscription', 'updated_at', 'phone_number', 'is_verified']
    
admin.site.register(CustomUser, CustomUserAdmin)