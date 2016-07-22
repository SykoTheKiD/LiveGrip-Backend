from rest_framework import permissions

from django.utils import timezone

from api.models import User, AccessToken
from api.authenticators import ExpiringTokenAuthentication

class IsValidToken(permissions.BasePermission):
	message = "Invalid Token"

	def has_permission(self, request, view):
		request_token = request.META['HTTP_AUTHORIZATION'].split()[1]
		user = None
		try:
			user = request.data['user_id']
		except KeyError:
			return False
		try:
			db_token = AccessToken.objects.get(key=request_token, user=user)
			if(db_token.created < timezone.now()):
				return False
			else:
				return True
		except AccessToken.DoesNotExist:
			return False

class IsActive(permissions.BasePermission):
		message = "Account Blocked"

		def has_permission(self, request, view):
			try:
				user = request.data['user_id']
			except KeyError:
				return False
			try:
				db_user = User.objects.get(id=user)
				return db_user.is_active
			except User.DoesNotExist:
				return False