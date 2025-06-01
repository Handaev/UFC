from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_fighter', 'is_manager', 'is_staff', 'is_active')
    list_filter = ('is_fighter', 'is_manager', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_fighter', 'is_manager')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
