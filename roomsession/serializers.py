from reactions.serializers import SessionFeedbackSerializer
from reactions.serializers import SessionFeedback
from django.utils.crypto import get_random_string
from rest_framework import serializers
from roomsession.models import RoomSession, SessionDate
from tags.models import Tags
from django.utils import timezone
from datetime import timedelta

from reactions.models import Likes, Follow
from accounts.serializers import UserModel
from datetime import datetime
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from accounts.serializers import UserDetailsSerializer


class SessionDateSerializer(serializers.ModelSerializer):
    session_date = serializers.DateField(format="%Y-%m-%dT%H:%M")
    formatted_session_date = serializers.SerializerMethodField()

    class Meta:
        model = SessionDate
        fields = ('id', 'session_date', 'reserved', 'deruration', 'price',
                  'reserver', 'formatted_session_date')

    def get_formatted_session_date(self, obj):
        return obj.session_date.strftime("%B %d, %Y at %I:%M %p")
    # def create(self, validated_data):
    #     session_date_str = validated_data.get('session_date')
    #     session_date = datetime.strptime(session_date_str, "%Y-%m-%dT%H:%M:%S")


class UserSerializer(serializers.ModelSerializer):
    followed_by_user = serializers.SerializerMethodField()

    def get_followed_by_user(self, obj):
        user = self.context['request'].user
        print('-------------user-----------', user)
        try:
            follow = Follow.get_is_follow_mentor(
                student=user, following_mentor=obj)
            return follow.isfollow
        except Follow.DoesNotExist:
            return False

    class Meta:
        model = UserModel
        fields = ('user_id', 'email', 'username', 'name', 'bio', 'phone', 'date_birth', 'followed_by_user',
                  'facebook_link', 'github_link', 'instgram_link', 'user_profile')


class SessionViewSerializer(serializers.ModelSerializer):
    available_dates = SessionDateSerializer(many=True, read_only=True)
    # tags=TagSerializer(many=True, read_only=True)
    mentor = UserSerializer()
    # created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField(format='%d %b')
    # user_bio = serializers.SerializerMethodField(read_only=True)
    # bio = serializers.CharField(source='bio', read_only=True)
    time_since_created = serializers.SerializerMethodField()
    session_feedback = SessionFeedbackSerializer(many=True, read_only=True)
    user_feedback = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField()
    session_dates_count = serializers.SerializerMethodField()

    def get_session_dates_count(self, obj):
        return obj.available_dates.count()

    def get_user_feedback(self, obj):
        user = self.context['request'].user  # get_user_feedback_about_session
        print('-------------user-----------', self.context['request'])
        print('-------------user-----------', obj)
        submit_session = SessionFeedback.objects.filter(
            student=user, session=obj)
        print('-------------user-----------',
              submit_session.exists())
        return submit_session.exists()

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
        fields = ('id', 'title', 'available_dates', 'mentor', 'description',
                  'session_feedback', 'user_feedback', 'session_dates_count',
                  'ended_at', 'sessionUrl', 'tags', 'updated_at', 'created_at', 'time_since_created',)
        # depth = 1

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
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50), write_only=True
    )

    class Meta:
        model = RoomSession
        fields = ('title', 'available_dates',
                  'ended_at', 'sessionUrl', 'tags', 'updated_at')

    # def create(self, validated_data):
    #     tag_names = validated_data.pop("tags")
    #     room_session = RoomSession.objects.create(**validated_data)

    #     for tag_name in tag_names:
    #         tag, created = Tags.objects.get_or_create(caption=tag_name)
    #         room_session.tags.add(tag)

    #     return room_session


class SessionSerializer(serializers.ModelSerializer):
    available_dates = SessionDateSerializer(many=True, read_only=True)

    class Meta:
        model = RoomSession
        fields = ('title', 'available_dates', 'mentor',
                  'ended_at', 'sessionUrl', 'tags')

    def validate_ended_at(self, value):
        """
        Check that end_date is not in the past.
        """
        if value < timezone.now().date():
            raise serializers.ValidationError(
                "End date cannot be in the past.")
        return value

    def create(self, validated_data):
        print('generate session_url')
        session_url_code = 'rs{}{}'.format(validated_data['mentor'],
                                           get_random_string(length=20))

        # validated_data[
        #     'sessionUrl'] = f"http://127.0.0.1:8000/roomsession/hall/{get_random_string(length=20)}{validated_data['mentor']}"

        validated_data[
            'sessionUrl'] = f"http://localhost:3000/room/{session_url_code}"
        return super().create(validated_data)


class singleDateSerilizer(serializers.ModelSerializer):
    reserver = UserDetailsSerializer()

    class Meta:

        model = SessionDate
        fields = "__all__"


class RoomSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomSession
        fields = '__all__'


# mentor short selizer data
class CustomeMentorSelizer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('email', 'username', 'name', 'user_profile')


class CustomeRoomSessionSelizer(serializers.ModelSerializer):
    mentor = CustomeMentorSelizer()

    class Meta:
        model = RoomSession
        fields = ['title', 'mentor', 'sessionUrl', 'description']


class UserPickedSessions(serializers.ModelSerializer):
    session_room = serializers.SerializerMethodField()
    formatted_session_date = serializers.SerializerMethodField()

    def get_formatted_session_date(self, obj):
        return obj.session_date.strftime("%B %d, %Y at %I:%M %p")

    def get_session_room(self, obj):
        try:
            print("obj__________________", obj)
            room = RoomSession.objects.filter(available_dates=obj).first()

            print('room_________________________', room)
            return CustomeRoomSessionSelizer(instance=room).data
        except:
            return None

    class Meta:
        model = SessionDate
        fields = ['session_room', 'session_date',
                  'reserved', 'reserver', 'deruration', 'formatted_session_date']
