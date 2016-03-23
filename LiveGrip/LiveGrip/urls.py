from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/login', 'api.views.login', name='login'),
	url(r'^auth/sign_up', 'api.views.sign_up', name='sign_up'),
	url(r'^events/$', 'api.views.events', name='events'),
    url(r'^messages/(?P<event_id>[0-9]+)$', 'api.views.messages', name='saved_messages'),
]
