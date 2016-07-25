from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import User, Event

## Constants
USERNAME = 'username'
PASSWORD = 'password'
PROFILE_IMAGE = 'profile_image'

## VALID DUMMY DATA
VALID_LOGIN_DATA = {USERNAME: 'JaySyko', PASSWORD: 'passpass'}
VALID_REGISTER_DATA = {USERNAME: 'JaySyko', PASSWORD: 'passpass', PROFILE_IMAGE:'image.jpg'}

## URLS
REGISTER = 'register'
LOGIN = 'login'
EVENTS = 'events&app_version=2'
UPDATE_PROFILE_IMAGE = 'updateProfileImage'
HTTP_AUTHORIZATION = 'HTTP_AUTHORIZATION'

RESPONSE_DATA = 'data'
RESPONSE_TOKEN = 'token'
AUTH_PREFIX = 'Token '
RESPONSE_DATA_ID = 'id'

## Util Functions
def makePostRequest(url, authInfo, client):
    url = reverse(url)
    return client.post(url, authInfo, format='json')

def makeGetRequest(endpoint, client):
    url = "http://localhost:3000/" + endpoint
    return client.get(url, format='json')


class NonAuthorizedTests(APITestCase):
    """
    Register user tests
    """
    def test_create_account_complete(self):
        """
        Ensure we can create a new account object.
        """
        response = makePostRequest(REGISTER, VALID_REGISTER_DATA, self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, VALID_REGISTER_DATA[USERNAME])

    def test_create_account_default_profile_image(self):
        """
        Ensure we can create a new account object.
        """
        data = {USERNAME: 'JaySyko', PASSWORD: 'passpass'}
        response = makePostRequest(REGISTER, data, self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'JaySyko')

    def test_create_account_bad_data(self):
        """
        Ensure we can create a new account object.
        """
        data = {USERNAME: 'kanye'}
        response = makePostRequest(REGISTER, data, self.client)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    """
    Login user tests
    """
    def test_login_bad_data(self):
        """
        Ensure we can create a new account object.
        """
        data = {'dummy': 'data'}
        response = makePostRequest(LOGIN, data, self.client)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_not_found(self):
        """
        Ensure we can create a new account object.
        """
        data = {USERNAME: 'sethrollins', PASSWORD: 'theshield'}
        response = makePostRequest(LOGIN, data, self.client)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_login_disabled_user(self):
        """
        Ensure we can create a new account object.
        """
        REQUEST_CLIENT = self.client
        registerResponse = makePostRequest(REGISTER, VALID_REGISTER_DATA, REQUEST_CLIENT)
        user = User.objects.get()
        user.is_active = False
        user.save()
        response = makePostRequest(LOGIN, VALID_LOGIN_DATA, REQUEST_CLIENT)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_good(self):
        """
        Ensure we can create a new account object.
        """
        REQUEST_CLIENT = self.client
        registerResponse = makePostRequest(REGISTER, VALID_REGISTER_DATA, REQUEST_CLIENT)
        self.assertEqual(registerResponse.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'JaySyko')

        response = makePostRequest(LOGIN, VALID_LOGIN_DATA, REQUEST_CLIENT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class AuthorizedTests(APITestCase):

    def test_update_image_bad_request(self):
        """
        Ensure we can reject a bad image update request properly.
        """
        REQUEST_CLIENT = self.client
        response = makePostRequest(REGISTER, VALID_REGISTER_DATA, REQUEST_CLIENT)
        authToken = response.data[RESPONSE_DATA][RESPONSE_TOKEN]
        
        REQUEST_CLIENT.defaults[HTTP_AUTHORIZATION] = AUTH_PREFIX + authToken
        test_response = makePostRequest(UPDATE_PROFILE_IMAGE, {'user_id': 1}, REQUEST_CLIENT)
        # self.assertEqual(test_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(test_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_image_good(self):
        """
        Ensure we can update a user's profile image.
        """
        REQUEST_CLIENT = self.client
        response = makePostRequest(REGISTER, VALID_REGISTER_DATA, REQUEST_CLIENT)
        authToken = response.data[RESPONSE_DATA][RESPONSE_TOKEN]
        REQUEST_CLIENT.defaults[HTTP_AUTHORIZATION] = AUTH_PREFIX + authToken

        test_response = makePostRequest(UPDATE_PROFILE_IMAGE, {'user_id': response.data[RESPONSE_DATA][RESPONSE_DATA_ID], PROFILE_IMAGE:'image.jpg'}, REQUEST_CLIENT)
        self.assertEqual(test_response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get().profile_image, 'image.jpg')

    def test_update_image_not_found(self):
        """
        Ensure we can create a new account object.
        """
        REQUEST_CLIENT = self.client
        response = makePostRequest(REGISTER, VALID_REGISTER_DATA, REQUEST_CLIENT)
        authToken = response.data[RESPONSE_DATA][RESPONSE_TOKEN]
        REQUEST_CLIENT.defaults[HTTP_AUTHORIZATION] = AUTH_PREFIX + authToken

        test_response = makePostRequest(UPDATE_PROFILE_IMAGE, {'user_id': 5, PROFILE_IMAGE:'image.jpg'}, REQUEST_CLIENT)
        # self.assertEqual(test_response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(test_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_events(self):
        REQUEST_CLIENT = self.client
        response = makePostRequest(REGISTER, VALID_REGISTER_DATA, REQUEST_CLIENT)
        authToken = response.data[RESPONSE_DATA][RESPONSE_TOKEN]
        REQUEST_CLIENT.defaults[HTTP_AUTHORIZATION] = AUTH_PREFIX + authToken

        test_response = makeGetRequest(EVENTS, REQUEST_CLIENT)
        self.assertEqual(test_response.status_code, status.HTTP_200_OK)