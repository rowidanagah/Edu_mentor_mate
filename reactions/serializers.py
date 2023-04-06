from accounts.serializers import UserModel
from .models import Likes, Follow, SessionFeedback

from rest_framework import serializers


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = ['isLike', 'blog', 'user']


class followSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('following_mentor', 'student', 'isfollow')

    def validate(self, data):
        print('-----------------', data['following_mentor'])

        if data['student'] == data['following_mentor']:
            raise serializers.ValidationError(
                "A user cannot follow themselves.")
        return data


class UserFeedbackSerializer(serializers.ModelSerializer):
    # user_feedback = serializers.SerializerMethodField()

    # def get_user_feedback(self, obj):
    #     user = self.context['request'].user  # get_user_feedback_about_session
    #     print('-------------user-----------', self.context['request'])
    #     print('-------------user-----------', obj)
    #     print('-------------user-----------',
    #           SessionFeedback.objects.filter(student=user, session=obj))
    #     return False
    #     # try:
    #     #     follow = Follow.get_is_follow_mentor(
    #     #         student=user, following_mentor=obj)
    #     #     return follow.isfollow
    #     # except Follow.DoesNotExist:
    #     #     return False
    #     # return False

    class Meta:
        model = UserModel
        fields = ('user_id', 'email', 'username', 'name', 'bio', 'phone', 'date_birth',
                  'facebook_link', 'github_link', 'instgram_link', 'user_profile')

# Session feedback


class SessionFeedbackSerializer(serializers.ModelSerializer):
    student = UserFeedbackSerializer()

    class Meta:
        model = SessionFeedback
        fields = ('student', 'massage', 'session')


class SessionFeedbackCReateSerializer(serializers.ModelSerializer):

    class Meta:
        model = SessionFeedback
        fields = '__all__'
