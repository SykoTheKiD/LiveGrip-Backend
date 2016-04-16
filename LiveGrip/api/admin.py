from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from api.models import *

from copy import deepcopy

## Admin Managers
class UserAdmin(admin.ModelAdmin):
	list_display = ('id', 'username', 'password', 'profile_image', 'gcm_id', 'app_version', 'last_login', 'is_active', 'date_joined')

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

	def sendGCM(self, request, queryset):
		rows_updated = queryset.update(is_active=True)
		if rows_updated == 1:
			message_bit = "1 User was sent"
		else:
			message_bit = "%s Users were sent" % rows_updated
		self.message_user(request, "%s a Google Cloud Message." % message_bit)

	sendGCM.short_description = "Send Cloud Message To Selected Users"

	actions = [activateAccount, disableAccount, sendGCM]
    
class EventAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Event._meta.fields]

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

## Regsiter to Admin
admin.site.register(User, UserAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Message)