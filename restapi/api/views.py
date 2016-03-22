from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from models import *
from serializers import *

@api_view(['POST'])
def sign_up(request):
    """
    List all tasks, or create a new task.
    """
    serializer = UserSerializer(data=request.DATA)
    if serializer.is_valid():
    	serializer.save()
    	return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request, username, password):
    """
    List all tasks, or create a new task.
    """
    try:
    	user = User.objects.get(username=username, password=password)
    except User.DoesNotExist:
    	return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def events(request):
    """
    List all tasks, or create a new task.
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
def message(request, event_id):
    """
    List all tasks, or create a new task.
    """
    if request.method == 'GET':
        events = Event.objects.get(event_id=event_id)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EventSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
    	pass
