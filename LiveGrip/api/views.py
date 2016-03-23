from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import *
from api.serializers import *

from django.http import HttpResponse

responseTemplate = {'payload': None}
STATUS = "status"
PAYLOAD = "payload"


@api_view(['POST'])
def sign_up(request):
    """
    Create a new User
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
    	serializer.save()
        # responseTemplate[STATUS]=status.HTTP_201_CREATED
        responseTemplate[PAYLOAD]=serializer.data
        return Response(responseTemplate,status=status.HTTP_201_CREATED)
    else:
        # responseTemplate[STATUS] = status.HTTP_400_BAD_REQUEST
        responseTemplate[PAYLOAD] = serializer.errors
        return Response(responseTemplate, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    """
    Login a new User
    """
    try:
        username = request.data.get("username", None)
        password = request.data.get("password", None)
        if(username == None or password == None):
            raise User.DoesNotExist
    	user = User.objects.get(username=username, password=password)
    except User.DoesNotExist:
    	return Response(responseTemplate, status=status.HTTP_200_OK)
    serializer = UserSerializer(user)
    responseTemplate[PAYLOAD] = serializer.data
    return Response(responseTemplate, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def events(request):
    """
    List all the Events
    """
    if request.method == 'GET':
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        # responseTemplate[STATUS] = status.HTTP_200_OK
        responseTemplate[PAYLOAD] = serializer.data
        return Response(responseTemplate, status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # responseTemplate[STATUS] = status.HTTP_201_CREATED
            return Response(responseTemplate, status=status.HTTP_201_CREATED)
        else:
            # responseTemplate[STATUS] = status.HTTP_400_BAD_REQUEST
            responseTemplate[PAYLOAD] = serializer.errors
            return Response(responseTemplate, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
def messages(request, event_id):
    """
    List all messages given a certain event
    """
    # event_id = request.data.get("event_id", None)
    if request.method == 'GET':
        events = Message.objects.filter(event=1).values('user') 
        # events = Message.objects.all()
        serializer = MessageSerializer(events, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MessageSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
    	pass