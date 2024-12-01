from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

# Register your models here.
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ["email", "username", "is_verified"]


admin.site.register(User, CustomUserAdmin)
