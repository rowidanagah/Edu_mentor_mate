from blogs.models import BLog
from rest_framework import serializers
from accounts.serializers import UserSerializer
from roomsession.serializers import BlogSessionSerializer
from django.utils import timezone
from datetime import timedelta


class BlogModelSerializer(serializers.ModelSerializer):
    mentor = UserSerializer()
    session = BlogSessionSerializer()
    cover_image = serializers.ImageField(required=False)
    time_since_created = serializers.SerializerMethodField()

    def get_time_since_created(self, obj):
        now = timezone.now()
        time_since = now - obj.updated_at
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
        model = BLog
        fields = ('id', 'title', 'content', 'mentor', 'updated_at',
                  'cover_image', 'created_at', 'tags', 'session', 'updated_at', 'time_since_created')

    # def get_cover_image(self, obj):
    #     if obj.cover_image:
    #         print('------------------', self.context['request'].build_absolute_uri(obj.cover_image.url))

    #         return self.context['request'].build_absolute_uri(obj.cover_image.url)
    #     return ''
