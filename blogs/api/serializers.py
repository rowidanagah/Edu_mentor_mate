from blogs.models import BLog
from rest_framework import serializers
from accounts.serializers import UserSerializer
from roomsession.serializers import BlogSessionSerializer


class BlogModelSerializer(serializers.ModelSerializer):
    mentor = UserSerializer()
    session = BlogSessionSerializer()
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = BLog
        fields = ('id', 'title', 'content', 'mentor', 'updated_at',
                  'cover_image', 'created_at', 'tags', 'session', 'updated_at')

    def get_cover_image(self, obj):
        if obj.cover_image:
            print('------------------', self.context['request'].build_absolute_uri(obj.cover_image.url))

            return self.context['request'].build_absolute_uri(obj.cover_image.url)
        return ''
