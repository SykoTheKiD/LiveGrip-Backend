from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import User, Event

## Constants
USERNAME = 'username'
PASSWORD = 'password'
PROFILE_IMAGE = 'profile_image'

## VALID DUMMY DATA
VALID_LOGIN_DATA = {USERNAME: 'JaySyko', PASSWORD: 'passpass', 'app_version': "1.00"}
VALID_REGISTER_DATA = {USERNAME: 'JaySyko', PASSWORD: 'passpass', PROFILE_IMAGE:'image.jpg', 'app_version': "1.00"}

## URLS
HOST = "http://localhost:3000/"
API_VERSION = 'v1/'
# URL Endpoints
REGISTER = 'auth/register'
LOGIN = 'auth/login'
EVENTS = 'events'
UPDATE_PROFILE_IMAGE = 'user/update/profile_image'
# HTTP HEADER Keys
HTTP_AUTHORIZATION = 'HTTP_AUTHORIZATION'

RESPONSE_DATA = 'data'
RESPONSE_TOKEN = 'token'
AUTH_PREFIX = 'Token '
RESPONSE_DATA_ID = 'id'
TOKEN_KEY = 'key'

## Util Functions
def post(endpoint, authInfo, client):
    url = HOST + API_VERSION + endpoint
    return client.post(url, authInfo, format='json')

def get(endpoint, client):
    url = HOST + API_VERSION + endpoint
    return client.get(url, format='json')

class NonAuthorizedTests(APITestCase):
    """
    Register user tests
    """
    def test_create_account_complete(self):
        """
        Ensure we can create a new account object.
        """
        response = post(REGISTER, VALID_REGISTER_DATA, self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, VALID_REGISTER_DATA[USERNAME])

    def test_create_account_default_profile_image(self):
        """
        Ensure we can create a new account object.
        """
        data = {USERNAME: 'JaySyko', PASSWORD: 'passpass', 'app_version': "1.00"}
        response = post(REGISTER, data, self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'JaySyko')

    def test_create_account_bad_data(self):
        """
        Ensure we can create a new account object.
        """
        data = {USERNAME: 'kanye'}
        response = post(REGISTER, data, self.client)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     """
#     Login user tests
#     """
    def test_login_bad_data(self):
        """
        Ensure we can create a new account object.
        """
        data = {'dummy': 'data'}
        response = post(LOGIN, data, self.client)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_not_found(self):
        """
        Ensure we can create a new account object.
        """
        data = {USERNAME: 'sethrollins', PASSWORD: 'theshield'}
        response = post(LOGIN, data, self.client)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_login_disabled_user(self):
        """
        Ensure we can create a new account object.
        """
        REQUEST_CLIENT = self.client
        registerResponse = post(REGISTER, VALID_REGISTER_DATA, REQUEST_CLIENT)
        user = User.objects.get()
        user.is_active = False
        user.save()
        response = post(LOGIN, VALID_LOGIN_DATA, REQUEST_CLIENT)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_good(self):
        """
        Ensure we can create a new account object.
        """
        REQUEST_CLIENT = self.client
        registerResponse = post(REGISTER, VALID_REGISTER_DATA, REQUEST_CLIENT)
        self.assertEqual(registerResponse.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'JaySyko')

        response = post(LOGIN, VALID_LOGIN_DATA, REQUEST_CLIENT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class AuthorizedTests(APITestCase):

    def setUp(self):
        global REQUEST_CLIENT
        global response
        REQUEST_CLIENT = self.client
        response = post(REGISTER, VALID_REGISTER_DATA, REQUEST_CLIENT)
        auth_token = AUTH_PREFIX + response.data[RESPONSE_DATA][RESPONSE_TOKEN][TOKEN_KEY]
        REQUEST_CLIENT.defaults[HTTP_AUTHORIZATION] = auth_token

    def test_update_image_bad_request(self):
        """
        Ensure we can reject a bad image update request properly.
        """        
        test_response = post(UPDATE_PROFILE_IMAGE, {'user_id': 12}, REQUEST_CLIENT)
        self.assertEqual(test_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_image_good(self):
        """
        Ensure we can update a user's profile image.
        """
        test_response = post(UPDATE_PROFILE_IMAGE, {'user_id': response.data[RESPONSE_DATA][RESPONSE_DATA_ID], PROFILE_IMAGE:'image.jpg'}, REQUEST_CLIENT)
        self.assertEqual(test_response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get().profile_image, 'image.jpg')

    def test_update_image_not_found(self):
        """
        Ensure we can create a new account object.
        """
        test_response = post(UPDATE_PROFILE_IMAGE, {'user_id': 5, PROFILE_IMAGE:'image.jpg'}, REQUEST_CLIENT)
        self.assertEqual(test_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_events(self):
        test_response = get(EVENTS, REQUEST_CLIENT)
        self.assertEqual(test_response.status_code, status.HTTP_200_OK)