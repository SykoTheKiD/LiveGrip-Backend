from django.conf.urls import url
from django.contrib import admin
from rest_framework.authtoken import views

import api.views

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^auth/login', api.views.login_user, name='login'),
	url(r'^auth/register', api.views.sign_up, name='register'),
	url(r'^events', api.views.events, name='events'),
	url(r'^user/update/profile_image', api.views.updateProfileImage, name='updateProfileImage'),
]
