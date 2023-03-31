from rest_framework import serializers
from roomsession.models import RoomSession, SessionDate
from accounts.serializers import UserSerializer
from tags.models import Tags
from django.utils import timezone
from datetime import timedelta


class SessionDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionDate
        fields = '__all__'

# class TagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tags
#         fields = ('caption',)


class SessionViewSerializer(serializers.ModelSerializer):
    available_dates = SessionDateSerializer(many=True, read_only=True)
    # tags=TagSerializer(many=True, read_only=True)
    mentor=UserSerializer()
    created_at = serializers.DateTimeField(format='%d %b')
    # user_bio = serializers.SerializerMethodField(read_only=True)
    # bio = serializers.CharField(source='bio', read_only=True)
    time_since_created = serializers.SerializerMethodField()

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
        model = RoomSession
        fields = ('title', 'available_dates', 'mentor',
                  'ended_at', 'sessionUrl', 'tags', 'deruration','updated_at','created_at','time_since_created',)
        #depth = 1

    # def create(self, validated_data):
    #     print("-------------validation------", validated_data)
    #     dates = validated_data.pop("available_dates")
    #     print("-------------------pop----------------", dates)
    #     session_rom = RoomSession.objects.create(**validated_data)
    #     return session_rom


class BlogSessionSerializer(serializers.ModelSerializer):
    available_dates = SessionDateSerializer(many=True, read_only=True)
    # user_bio = serializers.SerializerMethodField(read_only=True)
    # bio = serializers.CharField(source='bio', read_only=True)

    class Meta:
        model = RoomSession
        fields = ('title', 'available_dates',
                  'ended_at', 'sessionUrl', 'tags', 'deruration', 'updated_at')





class SessionSerializer(serializers.ModelSerializer):
    available_dates = SessionDateSerializer(many=True, read_only=True)

    class Meta:
        model = RoomSession
        fields = ('title', 'available_dates', 'mentor',
                  'ended_at', 'sessionUrl', 'tags', 'deruration')