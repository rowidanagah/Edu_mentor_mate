from roomsession.serializers import SessionSerializer
from roomsession.serializers import UserPickedSessions
from roomsession.models import RoomSession, SessionDate
from tags.models import Tags
from comments.serializer import CommentSerializer
from reactions.models import Likes, Follow
from blogs.models import BLog
from rest_framework import serializers
from accounts.serializers import UserModel
from roomsession.serializers import BlogSessionSerializer, SessionViewSerializer
from django.utils import timezone
from datetime import timedelta
from comments.models import Comment
from comments.serializer import CommentSerializer


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
                  'facebook_link', 'github_link', 'instgram_link', 'user_profile', 'favourite_bins')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'

# --------------- Create blog


class RoomSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomSession
        fields = ('id', 'title', 'description', 'ended_at')


class SessionDateSerializer:
    class Meta:
        model = SessionDate
        fields = "__all__"


class BlogModelSerializer(serializers.ModelSerializer):
    # tags = TagSerializer(many=True, read_only=False)
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50), write_only=True
    )

    class Meta:
        model = BLog
        fields = ('title', 'content', 'tags',
                  'mentor', 'session', 'cover_image')

    def validate(self, attrs):
        if 'content' not in attrs:
            raise serializers.ValidationError(
                {'content': 'content is required.'})

        if 'mentor' not in attrs:
            raise serializers.ValidationError(
                {'mentor': 'mentor is required.'})

        return attrs

    def create(self, validated_data):
        tag_names = validated_data.pop("tags")
        blog = BLog.objects.create(**validated_data)
        print('taggggggggggg', tag_names)
        for tag_name in tag_names:
            tag, created = Tags.objects.get_or_create(caption=tag_name)
            blog.tags.add(tag)

        return blog

    # def create(self, validated_data):
    #     tags_data = validated_data.pop('tags')
    #     blog = BLog.objects.create(**validated_data)
    #     for tag_data in tags_data:
    #         try:
    #             tag = Tags.objects.get(name=tag_data['name'])
    #             blog.tags.add(tag)
    #         except Tags.DoesNotExist:
    #             tag = Tags.objects.create(**tag_data)
    #             blog.tags.add(tag)
    #     return blog
    # def create(self, validated_data):
    #     tags_data = validated_data.pop('tags')
    #     blog = BLog.objects.create(**validated_data)
    #     for tag_data in tags_data:
    #         tag_name = tag_data['name']
    #         tag, created = Tags.objects.get_or_create(caption=tag_name)
    #         blog.tags.add(tag)
    #     return blog


class UserinfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'


class BlogTrendsModelSerializer(serializers.ModelSerializer):
    mentor = UserinfoSerializer()
    updated_at = serializers.DateTimeField(format='%d %b')

    class Meta:
        model = BLog
        fields = '__all__'


class BlogViewModelSerializer(serializers.ModelSerializer):
    mentor = UserSerializer()
    student_blog_comment = CommentSerializer(
        many=True, read_only=True)
    session = BlogSessionSerializer()
   # student_blog_comment = CommentSerializer(many=True, read_only=True)

    # cover_image = serializers.ImageField(required=False)
    time_since_created = serializers.SerializerMethodField()
    number_of_comments = serializers.SerializerMethodField()
    number_of_likes = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField(format='%d %b')

    def get_liked_by_user(self, obj):
        user = self.context['request'].user
        print('-------------user-----------', user)
        try:
            like = Likes.get_user_reaction_on_blog(user=user, blog=obj)
            print('----------------------------LIKE STATE', like)
            return like.isLike
        except Likes.DoesNotExist:
            return False

    def get_number_of_comments(self, obj):
        print('--------------obj---------------', obj)
        return Comment.get_blog_number_of_comments(blog=obj)

    def get_number_of_likes(self, obj):
        print('--------------obj---------------', obj)
        return Likes.get_blog_number_of_likes(blog=obj)

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
        fields = ('id',  'liked_by_user', 'title', 'content', 'mentor', 'updated_at', 'number_of_likes', 'student_blog_comment',
                  'cover_image', 'created_at', 'tags', 'session', 'updated_at', 'time_since_created', 'number_of_comments')

    # def get_cover_image(self, obj):
    #     if obj.cover_image:
    #         print('------------------', self.context['request'].build_absolute_uri(obj.cover_image.url))

    #         return self.context['request'].build_absolute_uri(obj.cover_image.url)
    #     return ''


class UserActivitiesSerializer(serializers.ModelSerializer):
    mentor_blog = BlogViewModelSerializer(many=True, read_only=True)
    mentor_session = SessionViewSerializer(many=True, read_only=True)
    number_of_follows = serializers.SerializerMethodField()
    number_of_blogs = serializers.SerializerMethodField()
    number_of_sessions = serializers.SerializerMethodField()
    followed_by_user = serializers.SerializerMethodField()
    # user_reserved_sessions = UserPickedSessions

    # def get_user_reserved_sessions(self, obj):
    #     return SessionDate.objects.filter(roomsession__mentor=obj, reserved=True)

    def get_followed_by_user(self, obj):
        user = self.context['request'].user
        print('-------------user-----------', user)
        try:
            follow = Follow.get_is_follow_mentor(
                student=user, following_mentor=obj)
            return follow.isfollow
        except Follow.DoesNotExist:
            return False

    def get_number_of_follows(self, obj):
        print('--------------obj---------------', obj)
        return Follow.gte_number_of_follow(user=obj)

    def get_number_of_sessions(self, obj):
        print('--------------user---------------', obj)
        return RoomSession.get_mentor_number_of_sessions(mentor=obj)

    def get_number_of_blogs(self, obj):
        print('--------------user---------------', obj)
        return BLog.get_mentor_number_of_blogs(mentor=obj)

    class Meta:
        model = UserModel
        fields = ('email', 'followed_by_user', 'username', 'name', 'bio', 'phone', 'number_of_follows', 'number_of_blogs', 'number_of_sessions',
                  'date_birth', 'facebook_link', 'github_link', 'instgram_link', 'mentor_session', 'mentor_blog', 'specializations', 'tools', 'user_profile', 'joinDate',)
