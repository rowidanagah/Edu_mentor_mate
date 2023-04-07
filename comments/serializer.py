from accounts.models import User
from .models import Comment
from accounts.serializers import UserSerializer
from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class CommentPostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = ('content', 'student', 'blog', 'created_at', 'id')


class CommentSerializer(serializers.ModelSerializer):
    student = UserSerializer()
    created_at = serializers.DateTimeField(format='%d %b')
    time_since_created = serializers.SerializerMethodField()
    # order comments by created_at field in descending order

    def get_time_since_created(self, obj):
        now = timezone.now()
        time_since = now - obj.created_at
        if time_since < timedelta(minutes=1):
            return "just now"
        elif time_since < timedelta(hours=1):
            minutes = int(time_since.total_seconds() / 60)
            return f"{minutes} min ago"
        elif time_since < timedelta(days=1):
            hours = int(time_since.total_seconds() / 3600)
            return f"{hours} hours ago"
        else:
            days = int(time_since.total_seconds() / 86400)
            return f"{days} days ago"

    class Meta:
        model = Comment
        fields = ('content', 'student', 'blog',
                  'created_at', 'time_since_created', 'id')
        ordering = ['-created_at']

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     if self.context.get('order_by') == 'title':
    #         queryset = queryset.order_by('title')
    #     elif self.context.get('order_by') == '-created_at':
    #         queryset = queryset.order_by('-created_at')
    #     return queryset
