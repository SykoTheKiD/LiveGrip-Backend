from django.conf.urls import url
from django.contrib import admin
from rest_framework.authtoken import views

import api.views

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^auth/login', api.views.login_user, name='login'),
	url(r'^auth/register', api.views.sign_up, name='register'),
	url(r'^events&app_version=(?P<app_version>[0-9]+)', api.views.events, name='events'),
	url(r'^messages&event=(?P<event_id>[0-9]+)', api.views.messages, name='get_messages'),
	url(r'^messages/save', api.views.save_message, name='save_message'),
	url(r'^user/update/profile_image', api.views.update_profile_image, name='update_profile_image'),
	url(r'^user/update/fcm', api.views.update_FCM_token, name='update_FCM_token'),
]
