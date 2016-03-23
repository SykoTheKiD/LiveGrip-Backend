from rest_framework import serializers
from models import *

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('username', 'password')



class EventSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		fields = ('name', 'info', 'image', 'location', 'start_time', 'end_time', 'match_card')


class MessageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Message
		fields = ('body')