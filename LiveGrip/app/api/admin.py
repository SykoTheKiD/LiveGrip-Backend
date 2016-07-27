from django.contrib import admin
from django.utils import timezone
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from rest_framework.authtoken.models import Token

from api.models import *
from api.utils import new_token_expiry_date

## Admin Managers
class UserAdmin(admin.ModelAdmin):
	list_display = ('id', 'username', 'password', 'profile_image', 'app_version' ,'last_login', 'is_active', 'date_joined')
	empty_value_display = '-empty-'
	list_display_links = ('username')

	def disableAccount(self, request, queryset):
		rows_updated = queryset.update(is_active=False)
		if rows_updated == 1:
			message_bit = "1 User was"
		else:
			message_bit = "%s Users were" % rows_updated
		self.message_user(request, "%s successfully disabled." % message_bit)

	disableAccount.short_description = "Disable Selected Users"

	def activateAccount(self, request, queryset):
		rows_updated = queryset.update(is_active=True)
		if rows_updated == 1:
			message_bit = "1 User was"
		else:
			message_bit = "%s Users were" % rows_updated
		self.message_user(request, "%s successfully activated." % message_bit)

	activateAccount.short_description = "Activate Selected Users"
	actions = [activateAccount, disableAccount]
    
class EventAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Event._meta.fields]
	empty_value_display = '-empty-'
	list_display_links = ('name')

	def duplicateEvent(self, request, queryset):
		for object in queryset:
			object.id = None
			object.save()
		if queryset.count() == 1:
			message_bit = "1 Event was"
		else:
			message_bit = "%s Events were" % rows_updated
		self.message_user(request, "%s successfully duplicated." % message_bit)
	duplicateEvent.short_description = "Duplicate Selected Records"
	
	def publish(self, request, queryset):
		rows_updated = queryset.update(status='p')
		if rows_updated == 1:
			message_bit = "1 Event was"
		else:
			message_bit = "%s Events were" % rows_updated
		self.message_user(request, "%s successfully marked as published." % message_bit)

	publish.short_description = "Make Selected Events Available to Public"
	actions = [publish, duplicateEvent]

class MessageAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Message._meta.fields]
	empty_value_display = '-empty-'

class AuthTokenAdmin(admin.ModelAdmin):
	list_display = [field.name for field in AccessToken._meta.fields]
	empty_value_display = '-empty-'
	list_display_links = ('key')

	def activate(self, request, queryset):
		rows_updated = queryset.update(expiry_date=new_token_expiry_date())
		if rows_updated == 1:
			message_bit = "1 Access Token was"
		else:
			message_bit = "%s Access Tokens were" % rows_updated
		self.message_user(request, "%s successfully activated." % message_bit)

	activate.short_description = "Activate selected Access Tokens"

	def deactivate(self, request, queryset):
		rows_updated = queryset.update(expiry_date=timezone.now())
		if rows_updated == 1:
			message_bit = "1 Access Token was"
		else:
			message_bit = "%s Access Tokens were" % rows_updated
		self.message_user(request, "%s successfully deactivated." % message_bit)

	deactivate.short_description = "Deactivate selected Access Tokens"

	actions = [activate, deactivate]

class FirebaseTokenAdmin(admin.ModelAdmin):
	list_display = [field.name for field in FirebaseMessagingToken._meta.fields]
	empty_value_display = '-empty-'
	list_display_links = ('fcm_key')
## Regsiter to Admin
admin.site.register(User, UserAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(AccessToken, AuthTokenAdmin)
admin.site.register(FirebaseMessagingToken, FirebaseTokenAdmin)

admin.site.unregister(Group)
admin.site.unregister(Token)