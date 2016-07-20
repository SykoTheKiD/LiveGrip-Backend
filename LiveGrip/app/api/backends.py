from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class CaseInsensitiveModelBackend(ModelBackend):
	def authenticate(self, username=None, password=None):
		try:
			User = get_user_model()
			user = User.objects.get(username__iexact=username)
			if user.check_password(password):
				return user
			else:
				return None
		except User.DoesNotExist:
			return None