from reactions.models import Likes, Follow
from blogs.models import BLog
from rest_framework import serializers
from accounts.serializers import UserModel
from roomsession.serializers import BlogSessionSerializer
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
                  'facebook_link', 'github_link', 'instgram_link', 'user_profile')


class BlogModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BLog
        fields = '__all__'


class BlogViewModelSerializer(serializers.ModelSerializer):
    mentor = UserSerializer()
    student_blog_comment = CommentSerializer(many=True, read_only=True)
    session = BlogSessionSerializer()
    # cover_image = serializers.ImageField(required=False)
    time_since_created = serializers.SerializerMethodField()
    number_of_comments = serializers.SerializerMethodField()
    number_of_likes = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format='%d %b')

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
        fields = ('id',  'liked_by_user', 'title', 'content', 'mentor', 'updated_at', 'number_of_likes','student_blog_comment',
                  'cover_image', 'created_at', 'tags', 'session', 'updated_at', 'time_since_created', 'number_of_comments')

    # def get_cover_image(self, obj):
    #     if obj.cover_image:
    #         print('------------------', self.context['request'].build_absolute_uri(obj.cover_image.url))

    #         return self.context['request'].build_absolute_uri(obj.cover_image.url)
    #     return ''
