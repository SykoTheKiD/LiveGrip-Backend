from rest_framework import permissions

from django.utils import timezone

from api.models import User, AccessToken
from api.authenticators import ExpiringTokenAuthentication

class IsValidToken(permissions.BasePermission):
	message = "Invalid Token"

	def has_permission(self, request, view):
		try:
			user = request.data['user_id']
			db_token = AccessToken.objects.get(key=request.auth, user=user)
			if(db_token.expiry_date < timezone.now()):
				return False
			else:
				return True
		except Exception:
			return False

class IsActive(permissions.BasePermission):
		message = "Account Blocked"

		def has_permission(self, request, view):
			return request.user.is_active