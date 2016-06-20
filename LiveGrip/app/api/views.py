from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token as AuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer

from api.models import *
from api.serializers import *

from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render


"""
Public API for LiveGrip
@author: Jay Syko

TODO: Implement Auth Token
"""

# Constants
STATUS = 'status'
DATA = 'data'
SUCCESS = 'success'
FAIL = 'fail'
MESSAGE = 'message'

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
            JSON_RESPONSE[STATUS] = SUCCESS
            JSON_RESPONSE[DATA] = UserSerializer(user).data
            return Response(JSON_RESPONSE, status=status.HTTP_201_CREATED)
    JSON_RESPONSE[STATUS] = FAIL
    JSON_RESPONSE[MESSAGE] = serializer.errors
    return Response(JSON_RESPONSE, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
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
                tokenSerializer = AuthTokenSerializer(data=request.data)
                tokenSerializer.is_valid()
                userToken = tokenSerializer.validated_data['user']
                token, created = AuthToken.objects.get_or_create(user=userToken)
                update_last_login(None, user)
                JSON_RESPONSE[STATUS] = SUCCESS
                JSON_RESPONSE[DATA] = serializer.data
                JSON_RESPONSE[DATA]["token"] = token.key
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
def updateProfileImage(request):
    """
    Update the user's profile image
    """
    JSON_RESPONSE = {STATUS: None, DATA: None, MESSAGE: None}
    try:
        username=request.data['username']
        profile_image = request.data['profile_image']
        try:
            user = User.objects.get(username=username)
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
def events(request):
    """
    List all the Events
    """
    JSON_RESPONSE = {STATUS: None, DATA: None, MESSAGE: None}
    if request.method == 'GET':
        JSON_RESPONSE[STATUS] = SUCCESS
        events = Event.objects.filter(status = 'p')
        serializer = EventSerializer(events, many=True)
        JSON_RESPONSE[DATA] = serializer.data
        return Response(JSON_RESPONSE, status=status.HTTP_200_OK)

@api_view(['GET'])
def messages(request, event_id):
    """
    List all messages given a certain event
    """
    JSON_RESPONSE = {STATUS: None, DATA: None, MESSAGE: None}
    messages = Message.objects.filter(event=event_id)[:50]
    serializer = GetMessageSerializer(messages, many=True)
    JSON_RESPONSE[STATUS] = SUCCESS
    JSON_RESPONSE[DATA] = serializer.data
    return Response(JSON_RESPONSE, status=status.HTTP_200_OK)

@api_view(['POST'])
def saveMessage(request):
    JSON_RESPONSE = {STATUS: None, DATA: None, MESSAGE: None}
    serializer = SaveMessageSerializer(data=request.data)
    if serializer.is_valid():
        JSON_RESPONSE[STATUS] = SUCCESS
        JSON_RESPONSE[MESSAGE] = "Saved" 
        serializer.save()
        return Response(JSON_RESPONSE, status=status.HTTP_201_CREATED)
    else:
        JSON_RESPONSE[STATUS] = FAIL
        JSON_RESPONSE[MESSAGE] = serializer.errors
        return Response(JSON_RESPONSE, status=status.HTTP_400_BAD_REQUEST)