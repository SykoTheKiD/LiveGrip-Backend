from rest_framework.views import exception_handler
from rest_framework.response import Response

STATUS = 'status'
DATA = 'data'
DETAIL = 'detail'
FAIL = 'fail'
MESSAGE = 'message'

def custom_exception_handler(exc, context):
	# Call REST framework's default exception handler first,
	# to get the standard error response.
	response = exception_handler(exc, context)

	JSON_RESPONSE = {STATUS: None, DATA: None, MESSAGE: None}
	# Now add the HTTP status code to the response.
	if response is not None:
		JSON_RESPONSE[STATUS] = FAIL
		JSON_RESPONSE[MESSAGE] = response.data[DETAIL]
	
	return Response(JSON_RESPONSE, status=response.status_code)