from api.models import AccessToken
from rest_framework.authentication import TokenAuthentication

class ExpiringTokenAuthentication(TokenAuthentication):
	model = AccessToken