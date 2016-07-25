from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.models import *
from api.serializers import *
from api.permissions import *
from api.utils import new_token_expiry_date
from api.authenticators import ExpiringTokenAuthentication

from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

import time
import os

import rethinkdb as r

"""
Public API for LiveGrip
@author: Jay Syko
"""

# Constants
APP_VERSION = 1
STATUS = 'status'
DATA = 'data'
SUCCESS = 'success'
FAIL = 'fail'
MESSAGE = 'message'
TOKEN = 'token'

CONN = r.connect(host="rethinkdb", db='livegrip_messages') if os.getenv('CI') == 'false' else None

@api_view(['POST'])
@permission_classes((AllowAny,))
def sign_up(request):
    """
    Create a new User
    """
    JSON_RESPONSE = {STATUS: None, DATA: None, MESSAGE: None}
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.create(request.data)
        if(user != None):
            token = AccessToken.objects.get(user=user)
            token_dict = {'token': token.key, 'expiry_date':token.expiry_date}
            JSON_RESPONSE[STATUS] = SUCCESS
            JSON_RESPONSE[DATA] = UserSerializer(user).data
            JSON_RESPONSE[DATA][TOKEN] = token_dict
            return Response(JSON_RESPONSE, status=status.HTTP_201_CREATED)
    JSON_RESPONSE[STATUS] = FAIL
    JSON_RESPONSE[MESSAGE] = "Username has been taken"
    return Response(JSON_RESPONSE, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((AllowAny,))
def login_user(request):
    """
    Login a new User
    """ 
    JSON_RESPONSE = {STATUS: None, DATA: None, MESSAGE: None}
    try:
        user = authenticate(username=request.data['username'], password=request.data['password'])
        serializer = UserSerializer(user)
        if user is not None:
            if user.is_active:
                db_token = AccessToken.objects.get(user=user.id)
                db_token.key = AccessToken().generate_key()
                db_token.expiry_date = new_token_expiry_date()
                db_token.save()
                update_last_login(None, user)
                token_dict = {'token': db_token.key, 'expiry_date':db_token.expiry_date}
                JSON_RESPONSE[STATUS] = SUCCESS
                JSON_RESPONSE[DATA] = serializer.data
                JSON_RESPONSE[DATA][TOKEN] = token_dict
                return Response(JSON_RESPONSE, status=status.HTTP_200_OK)
            else:
                JSON_RESPONSE[STATUS] = FAIL
                JSON_RESPONSE[MESSAGE] = "Account has been disabled"
                return Response(JSON_RESPONSE, status=status.HTTP_401_UNAUTHORIZED)
        else:
            JSON_RESPONSE[STATUS] = FAIL
            JSON_RESPONSE[MESSAGE] = "User not found"
            return Response(JSON_RESPONSE, status=status.HTTP_404_NOT_FOUND)
    except KeyError:
        return Response(JSON_RESPONSE, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((IsAuthenticated,IsValidToken,IsActive,))
def updateProfileImage(request):
    """
    Update the user's profile image
    """
    JSON_RESPONSE = {STATUS: None, DATA: None, MESSAGE: None}
    try:
        user_id = request.data['user_id']
        profile_image = request.data['profile_image']
        try:
            user = User.objects.get(id=user_id)
            user.profile_image = profile_image
            user.save()
            JSON_RESPONSE[STATUS] = SUCCESS
            return Response(JSON_RESPONSE, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            JSON_RESPONSE[STATUS] = FAIL
            JSON_RESPONSE[MESSAGE] = "User not found"
            return Response(JSON_RESPONSE, status=status.HTTP_404_NOT_FOUND)
    except KeyError:
        return Response(JSON_RESPONSE, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes((IsAuthenticated,IsActive,))
def events(request, app_version):
    """
    List all the Events
    """
    JSON_RESPONSE = {STATUS: None, DATA: None, MESSAGE: None}
    JSON_RESPONSE[STATUS] = SUCCESS
    if (int(app_version) < APP_VERSION):
            JSON_RESPONSE[MESSAGE] = "A New Version of the App is Available"
    events = Event.objects.filter(status = 'p')
    serializer = EventSerializer(events, many=True)
    JSON_RESPONSE[DATA] = serializer.data
    return Response(JSON_RESPONSE, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((IsAuthenticated,IsActive,))
def messages(request, event_id):
    """
    List all messages given a certain event
    """
    JSON_RESPONSE = {STATUS: None, DATA: None, MESSAGE: None}
    table_name = "event_" + str(event_id)
    JSON_RESPONSE[STATUS] = SUCCESS
    JSON_RESPONSE[DATA] = r.table(table_name).order_by(r.desc('message_id')).limit(10).run(CONN)
    return Response(JSON_RESPONSE, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes((IsAuthenticated,IsValidToken,IsActive,))
def saveMessage(request):
    JSON_RESPONSE = {STATUS: None, DATA: None, MESSAGE: None}
    table_name = "event_" + str(request.data['event_id'])
    r.table(table_name).insert({ 
        'username': request.data['username'], 
        'profile_image': request.data['profile_image'], 
        'event_id': request.data['event_id'], 
        'user_id': request.data['user_id'],
        'body': request.data['body'],
        'message_id': int(round(time.time() * 1000))}).run(CONN)
    JSON_RESPONSE[STATUS] = SUCCESS
    JSON_RESPONSE[MESSAGE] = "Saved"
    return Response(JSON_RESPONSE, status=status.HTTP_201_CREATED)