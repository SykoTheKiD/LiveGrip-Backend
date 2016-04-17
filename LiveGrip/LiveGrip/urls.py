from django.conf.urls import url
from django.contrib import admin

import api.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/login', api.views.login_user, name='login'),
	url(r'^auth/register', api.views.sign_up, name='register'),
	url(r'^events', api.views.events, name='events'),
    url(r'^messages/event=(?P<event_id>[0-9]+)', api.views.messages, name='getMessages'),
    url(r'^messages/save', api.views.saveMessage, name='saveMessage'),
    url(r'^user/update/profile_image', api.views.updateProfileImage, name='updateProfileImage'),
    url(r'^user/update/gcm_id', api.views.updateGCMID, name='updateGCMID'),
]
