from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import User

# Register your models here.


class UserAdmin(UserAdmin):
    model = User
    list_display = ["username", "email", "is_verified"]


admin.site.register(User, UserAdmin)
