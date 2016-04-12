from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from api.models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'password', 'profile_image', 'gcm_id', 'app_version', 'last_login', 'is_active', 'date_joined')
    
admin.site.register(User, UserAdmin)
admin.site.register(Event)