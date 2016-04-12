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
        serializer.create(serializer.validated_data)
    	return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
    else:
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    """
    Login a new User
    """
    user = authenticate(username=request.data['username'], password=request.data['password'])
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponse('user_logged_in')
        else:
            return HttpResponse('user_banned')
    else:
        return HttpResponse('user_not_found')


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
        serializer = EventSerializer(data=request.data)
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
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
    	pass
