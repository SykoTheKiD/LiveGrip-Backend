from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from api.models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'password', 'profile_image', 'email', 'last_login', 'is_active', 'date_joined')
    
admin.site.register(User, UserAdmin)