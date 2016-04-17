from rest_framework import serializers

from models import Event, User, Message

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('username', 'profile_image')

	def create(self, validated_data):
		user = None
		try:
			username = validated_data['username']
			password = validated_data['password']
			user = User(username=username)
			user.set_password(password)
			try:
				profile_image = validated_data['profile_image']
				user.profile_image = profile_image
			except KeyError:
				user.profile_image = "DEFAULT"
			user.save()
			return user
		except KeyError:
			return user
			

class EventSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		fields = ('name', 'info', 'image','location', 'start_time', 'end_time', 'match_card')


class GetMessageSerializer(serializers.ModelSerializer):
	user = serializers.StringRelatedField()
	event = serializers.StringRelatedField()
	class Meta:
		model = Message
		fields = ('user', 'event', 'body')

class SaveMessageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Message
		fields = ('user', 'event', 'body')