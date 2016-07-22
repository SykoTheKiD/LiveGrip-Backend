from rest_framework import permissions

from django.utils import timezone

from api.models import User, AccessToken
from api.authenticators import ExpiringTokenAuthentication

class IsValidToken(permissions.BasePermission):
	message = "Invalid Token"

	def has_permission(self, request, view):
		request_token = request.auth.key
		user = None
		try:
			user = request.data['user_id']
			db_token = AccessToken.objects.get(key=request_token, user=user)
			if(db_token.expiry_date < timezone.now()):
				return False
			else:
				return True
		except Exception:
			return False

class IsActive(permissions.BasePermission):
		message = "Account Blocked"

		def has_permission(self, request, view):
			try:
				# user = request.data['user_id']
				# db_user = User.objects.get(id=user)
				return request.user.is_active
			except Exception:
				return False