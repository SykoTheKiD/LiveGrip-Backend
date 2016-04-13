from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Event, User
from api.serializers import EventSerializer, UserSerializer

from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist

# Constants
STATUS = 'status'
DATA = 'data'
SUCCESS = 'success'
FAIL = 'fail'
JSON_RESPONSE = {STATUS: None, DATA: None}

@api_view(['POST'])
def sign_up(request):
    """
    Create a new User
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.create(request.data)
        if(user != None):
            JSON_RESPONSE[STATUS] = SUCCESS
            JSON_RESPONSE[DATA] = serializer.validated_data
            return Response(JSON_RESPONSE, status=status.HTTP_201_CREATED)
    JSON_RESPONSE[STATUS] = FAIL
    JSON_RESPONSE[DATA] = serializer.errors
    return Response(JSON_RESPONSE, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    """
    Login a new User
    """ 
    try:
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user is not None:
            if user.is_active:
                JSON_RESPONSE[STATUS] = SUCCESS
                JSON_RESPONSE[DATA] = {'username':user.username, 'profile_image': user.profile_image, 'is_active': user.is_active}
                return Response(JSON_RESPONSE, status=status.HTTP_200_OK)
            else:
                JSON_RESPONSE[STATUS] = FAIL
                JSON_RESPONSE[DATA] = "Account has been disabled"
                return Response(JSON_RESPONSE, status=status.HTTP_401_UNAUTHORIZED)
        else:
            JSON_RESPONSE[STATUS] = FAIL
            JSON_RESPONSE[DATA] = "User not found"
            return Response(JSON_RESPONSE, status=status.HTTP_404_NOT_FOUND)
    except KeyError:
        return Response(JSON_RESPONSE, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def updateGCMID(request):
    """
    Add a GCM ID to the User
    """
    try:
        username=request.data['username']
        gcm_id = request.data['gcm_id']
        try:
            user = User.objects.get(username=username)
            user.gcm_id = gcm_id
            user.save()
            JSON_RESPONSE[STATUS] = SUCCESS
            return Response(JSON_RESPONSE, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(JSON_RESPONSE, status=status.HTTP_404_NOT_FOUND)
    except KeyError:
        return Response(JSON_RESPONSE, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def updateProfileImage(request):
    """
    Update the user's profile image
    """
    try:
        username=request.data['username']
        profile_image = request.data['profile_image']
        try:
            user = User.objects.get(username=username)
            user.profile_image = profile_image
            user.save()
            JSON_RESPONSE[STATUS] = SUCCESS
            JSON_RESPONSE[DATA] = None
            return Response(JSON_RESPONSE, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            JSON_RESPONSE[STATUS] = FAIL
            JSON_RESPONSE[STATUS] = None
            return Response(JSON_RESPONSE, status=status.HTTP_404_NOT_FOUND)
    except KeyError:
        return Response(JSON_RESPONSE, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def events(request):
    """
    List all the Events
    """
    if request.method == 'GET':
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        JSON_RESPONSE[STATUS] = SUCCESS
        JSON_RESPONSE[DATA] = serializer.validated_data
        return Response(JSON_RESPONSE, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            JSON_RESPONSE[STATUS] = SUCCESS
            JSON_RESPONSE[DATA] = serializer.validated_data
            serializer.save()
            return Response(JSON_RESPONSE, status=status.HTTP_201_CREATED)
        else:
            JSON_RESPONSE[STATUS] = FAIL
            JSON_RESPONSE[DATA] = serializer.errors
            return Response(JSON_RESPONSE, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def messages(request, event_id):
    """
    List all messages given a certain event
    """
    if request.method == 'GET':
        events = Event.objects.select_related(event_id=event_id)
        serializer = MessageSerializer(events, many=True)
        if serializer.is_valid():
            JSON_RESPONSE[STATUS] = SUCCESS
            JSON_RESPONSE[DATA] = serializer.validated_data
            return Response(JSON_RESPONSE, status=status.HTTP_200_OK)
        else:
            JSON_RESPONSE[STATUS] = FAIL
            JSON_RESPONSE[DATA] = serializer.errors
            return Response(JSON_RESPONSE, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            JSON_RESPONSE[STATUS] = SUCCESS
            JSON_RESPONSE[DATA] = serializer.validated_data
            serializer.save()
            return Response(JSON_RESPONSE, status=status.HTTP_201_CREATED)
        else:
            JSON_RESPONSE[STATUS] = FAIL
            JSON_RESPONSE[DATA] = serializer.errors
            return Response(JSON_RESPONSE, status=status.HTTP_400_BAD_REQUEST)
