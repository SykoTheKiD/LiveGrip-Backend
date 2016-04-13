from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import User, Event

## Constants
USERNAME = 'username'
PASSWORD = 'password'
GCM_ID = 'gcm_id'
PROFILE_IMAGE = 'profile_image'

## VALID DUMMY DATA
VALID_LOGIN_DATA = {USERNAME: 'JaySyko', PASSWORD: 'passpass'}
VALID_REGISTER_DATA = {USERNAME: 'JaySyko', PASSWORD: 'passpass', PROFILE_IMAGE:'image.jpg'}

## URLS
REGISTER = 'register'
LOGIN = 'login'
EVENTS = 'events'
UPDATE_PROFILE_IMAGE = 'updateProfileImage'
UPDATE_GCM_ID = 'updateGCMID'

## Util Functions
def makePostRequest(url, authInfo, client):
    url = reverse(url)
    return client.post(url, authInfo, format='json')

def makeGetRequest(url, authInfo, client):
    url = reverse(url)
    return client.get(url, format='json')


class UserTests(APITestCase):
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
        data = {USERNAME: 'data'}
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

    def test_update_image_bad_request(self):
        """
        Ensure we can create a new account object.
        """
        REQUEST_CLIENT = self.client
        makePostRequest(REGISTER, VALID_REGISTER_DATA, REQUEST_CLIENT)

        response = makePostRequest(UPDATE_PROFILE_IMAGE, {USERNAME: VALID_LOGIN_DATA[USERNAME]}, REQUEST_CLIENT)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_image_good(self):
        """
        Ensure we can create a new account object.
        """
        REQUEST_CLIENT = self.client
        makePostRequest(REGISTER, VALID_REGISTER_DATA, REQUEST_CLIENT)

        response = makePostRequest(UPDATE_PROFILE_IMAGE, {USERNAME: VALID_LOGIN_DATA[USERNAME], PROFILE_IMAGE:'image.jpg'}, REQUEST_CLIENT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_image_not_found(self):
        """
        Ensure we can create a new account object.
        """
        response = makePostRequest(UPDATE_PROFILE_IMAGE, {USERNAME: VALID_LOGIN_DATA[USERNAME], PROFILE_IMAGE:'image.jpg'}, self.client)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_gcm_id_not_found(self):
        """
        Ensure we can create a new account object.
        """
        response = makePostRequest(UPDATE_GCM_ID, {USERNAME: VALID_LOGIN_DATA[USERNAME], GCM_ID: '309053213'}, self.client)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_gcm_id_bad_request(self):
        """
        Ensure we can create a new account object.
        """
        REQUEST_CLIENT = self.client
        makePostRequest(REGISTER, VALID_REGISTER_DATA, REQUEST_CLIENT)

        response = makePostRequest(UPDATE_GCM_ID, {PASSWORD: 'password'}, self.client)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_gcm_id_good(self):
        """
        Ensure we can create a new account object.
        """
        REQUEST_CLIENT = self.client
        makePostRequest(REGISTER, VALID_REGISTER_DATA, REQUEST_CLIENT)

        response = makePostRequest(UPDATE_GCM_ID, {USERNAME: VALID_LOGIN_DATA[USERNAME], GCM_ID: '309053213'}, REQUEST_CLIENT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



