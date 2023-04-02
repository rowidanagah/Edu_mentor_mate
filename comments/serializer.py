from accounts.models import User
from .models import Comment
from accounts.serializers import UserSerializer
from rest_framework import serializers


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class CommentSerializer(serializers.ModelSerializer):
    # student = StudentSerializer()
   # student = UserSerializer()

    class Meta:
        model = Comment
        fields = ('content', 'student', 'blog')
