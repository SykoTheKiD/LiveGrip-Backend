from rest_framework import serializers
from models import *

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Message
		fields = '__all__'