from .models import Likes, Follow

from rest_framework import serializers


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = ['isLike', 'blog', 'user']


class followSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('following_mentor', 'student' , 'isfollow')

    def validate(self, data):
        print('-----------------', data['following_mentor'])
        
        if data['student'] == data['following_mentor']:
                raise serializers.ValidationError(
                    "A user cannot follow themselves.")
        return data
