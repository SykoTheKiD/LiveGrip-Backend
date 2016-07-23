from django.utils import timezone

import datetime

TOKEN_VALID_DATE = 30 # days

def new_token_expiry_date():
	"""
	Generates a new expiry date for a token
	"""
	return timezone.now() + datetime.timedelta(days=TOKEN_VALID_DATE)