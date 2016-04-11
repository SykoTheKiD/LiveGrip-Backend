from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Event
from api.serializers import EventSerializer, UserSerializer

from django.http import HttpResponse
from django.contrib.auth import authenticate, login

@api_view(['GET'])
def home(request):
    """
    Home
    """
    return HttpResponse('API Backend')

@api_view(['POST'])
def sign_up(request):
    """
    Create a new User
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
    	username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        # serializer.set_password(password)
        response = Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        serializer.save()
    	return response
    else:
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request, username, password):
    """
    Login a new User
    """
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user);
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def events(request):
    """
    List all the Events
    """
    if request.method == 'GET':
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EventSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def messages(request, event_id):
    """
    List all messages given a certain event
    """
    if request.method == 'GET':
        events = Event.objects.select_related(event_id=1)
        serializer = MessageSerializer(events, many=True)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MessageSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
    	pass