from rest_framework import serializers

from models import Event, User

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('username', 'password', 'profile_image', 'is_active')
	def create(self, validated_data):
		username = validated_data['username']
		user = User(username=username)
		user.set_password(validated_data['password'])
		user.profile_image = validated_data['profile_image']
		user.save()
		return user

class EventSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		fields = ('name', 'info', 'image', 'location', 'start_time', 'end_time', 'match_card')


# class MessageSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = Message
# 		fields = ('body')