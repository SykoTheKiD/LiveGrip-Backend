from django.conf.urls import url

urlpatterns = [
	'api.views',
	url(r'^auth/login', 'login', name='login'),
	url(r'^auth/sign_up', 'sign_up', name='sign_up'),
	url(r'^events/$', 'events', name='events'),
    url(r'^messages/(?P<event_id>[0-9]+)$', 'messages', name='saved_messages'),
]
