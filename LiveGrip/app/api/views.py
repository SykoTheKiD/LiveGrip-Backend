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
from django.conf import settings

import time
import os

import rethinkdb as r

"""
Public API for LiveGrip
@author: Jay Syko
"""

# Constants
STATUS = 'status'
DATA = 'data'
SUCCESS = 'success'
FAIL = 'fail'
MESSAGE = 'message'
TOKEN = 'token'
LAST_MESSAGES = 50
LAST_MESSAGES_OFFSET = 10

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
            update_last_login(None, user)
            token = AccessToken.objects.get(user=user)
            token_serializer = AccessTokenSerializer(token)
            JSON_RESPONSE[STATUS] = SUCCESS
            JSON_RESPONSE[DATA] = UserSerializer(user).data
            JSON_RESPONSE[DATA][TOKEN] = token_serializer.data
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
                user.app_version = request.data['app_version']
                user.save()
                db_token = AccessToken.objects.get(user=user.id)
                db_token.key = AccessToken().generate_key()
                db_token.expiry_date = new_token_expiry_date()
                db_token.save()
                token_serializer = AccessTokenSerializer(db_token)
                update_last_login(None, user)
                JSON_RESPONSE[STATUS] = SUCCESS
                JSON_RESPONSE[DATA] = serializer.data
                JSON_RESPONSE[DATA][TOKEN] = token_serializer.data
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
        JSON_RESPONSE[MESSAGE] = "bad request data"
        return Response(JSON_RESPONSE, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((IsAuthenticated,IsValidToken,IsActive,))
def update_profile_image(request):
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
def events(request):
    """
    List all the Events
    """
    JSON_RESPONSE = {STATUS: None, DATA: None, MESSAGE: None}
    JSON_RESPONSE[STATUS] = SUCCESS
    events = Event.objects.filter(status = 'p')
    serializer = EventSerializer(events, many=True)
    JSON_RESPONSE[DATA] = serializer.data
    return Response(JSON_RESPONSE, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((IsAuthenticated,IsActive,))
def get_last_messages(request, event_id):
    """
    List all messages given a certain event
    """
    JSON_RESPONSE = {STATUS: None, DATA: None, MESSAGE: None}
    table_name = "event_" + str(event_id)
    JSON_RESPONSE[STATUS] = SUCCESS
    JSON_RESPONSE[DATA] = r.table(table_name).order_by(r.desc('message_id')).limit(LAST_MESSAGES).run(CONN)
    return Response(JSON_RESPONSE, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((IsAuthenticated,IsActive,))
def get_messagage_history(request, event_id, offset):
    """
    Get last 10 messages from index
    """
    JSON_RESPONSE = {STATUS: None, DATA: None, MESSAGE: None}
    table_name = "event_" + str(event_id)
    skip_offset = LAST_MESSAGES + LAST_MESSAGES_OFFSET * int(offset)
    JSON_RESPONSE[STATUS] = SUCCESS
    JSON_RESPONSE[DATA] = r.table(table_name).order_by(r.desc('message_id')).skip(skip_offset).limit(LAST_MESSAGES_OFFSET).run(CONN)
    return Response(JSON_RESPONSE, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes((IsAuthenticated,IsValidToken,IsActive,))
def save_message(request):
    JSON_RESPONSE = {STATUS: None, DATA: None, MESSAGE: None}
    table_name = "event_" + str(request.data['event_id'])
    try:
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
    except Exception:
        JSON_RESPONSE[STATUS] = FAIL
        JSON_RESPONSE[MESSAGE] = "An error in your request"
        return Response(JSON_RESPONSE, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((IsAuthenticated,IsValidToken,IsActive,))
def update_FCM_token(request):
    JSON_RESPONSE = {STATUS: None, DATA: None, MESSAGE: None}
    try:
        user_id = request.data['user_id']
        token = request.data['access_token']
        user = User.objects.get(id=user_id)
        firebase_token = FirebaseMessagingToken.objects.update_or_create(user=user, defaults={'fcm_key': token})
        JSON_RESPONSE[STATUS] = SUCCESS        
        return Response(JSON_RESPONSE, status=status.HTTP_200_OK)
    except Exception:
        JSON_RESPONSE[STATUS] = FAIL
        JSON_RESPONSE[MESSAGE] = "An error in your request"
        return Response(JSON_RESPONSE, status=status.HTTP_400_BAD_REQUEST)