from dj_rest_auth.serializers import PasswordResetSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
import re
from django.core.exceptions import ValidationError

from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token
from tags.models import Specialization

UserModel = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'

    def create(self, clean_data):
        user_obj = UserModel.objects.create_user(
            email=clean_data['email'], password=clean_data['password'])
        user_obj.username = clean_data['username']
        user_obj.save()
        Token.objects.create(user=user_obj)
        return user_obj


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    ##

    def check_user(self, clean_data):
        user = authenticate(
            username=clean_data['email'], password=clean_data['password'])
        if not user:
            raise ValidationError('user not found')
        return user


# login view


class UserSerializer(serializers.ModelSerializer):
    # class Meta:
    #     model = UserModel
    #     fields = ('email', 'username', 'name', 'bio', 'phone', 'date_birth', 'user_id',
    #               'facebook_link', 'github_link', 'instgram_link', 'user_profile')
    #     # fields = "__all__"
    #     # exclude = ('password', )

    class Meta:
        model = UserModel
        fields = ('email', 'username', 'name', 'bio', 'phone', 'facebook_link',
                  'github_link', 'instgram_link', 'user_profile', 'usertype', 'user_id', 'favourite_bins')
        # fields = "__all__"
        # exclude = ('password', )


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('name', 'bio', 'phone', 'facebook_link',
                  'github_link', 'instgram_link', 'favourite_bins')

# custome specilization serlizer


class SpecilizationSerlizer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'

        # custome register serializer for DRF


class CustomRegisterSerializer(RegisterSerializer):

    name = serializers.CharField(max_length=50)
    phone = serializers.CharField(max_length=14)
    user_profile = serializers.ImageField()
    # date_birth = serializers.DateField()
    usertype = serializers.CharField()
    # facebook_link = serializers.URLField()
    # github_link = serializers.URLField()
    # instgram_link = serializers.URLField()
    # specializations=SpecilizationSerlizer()

    def custom_signup(self, request, user):
        user.name = self.validated_data.get('name', '')
        user.phone = self.validated_data.get('phone', '')
        user.user_profile = self.validated_data.get('user_profile', '')
        # user.date_birth = self.validated_data.get('date_birth', '')
        user.usertype = self.validated_data.get('usertype', '')
        # user.facebook_link=self.validated_data.get('facebook_link','')
        # user.github_link=self.validated_data.get('github_link','')
        # user.instgram_link=self.validated_data.get('instgram_link','')
        user.save()

        # ____________________________________________


# # user details override dj_rest_auth
#   name =serializers.CharField(max_length=50)
#   phone=serializers.CharField(max_length=14)
#   user_profile=serializers.ImageField()
#   date_birth = serializers.DateField()
#   usertype=serializers.CharField()

#   #facebook_link = serializers.URLField()
#   # github_link = serializers.URLField()
#   # instgram_link = serializers.URLField()
#   # specializations=SpecilizationSerlizer()

#   def custom_signup(self, request, user):
# 			user.name = self.validated_data.get('name', '')
# 			user.phone = self.validated_data.get('phone','')
# 			user.user_profile=self.validated_data.get('user_profile','')
# 			user.date_birth=self.validated_data.get('date_birth','')
# 			user.usertype=self.validated_data.get('usertype','')

# 			# user.facebook_link=self.validated_data.get('facebook_link','')
# 			# user.github_link=self.validated_data.get('github_link','')
# 			# user.instgram_link=self.validated_data.get('instgram_link','')
# 			user.save()

        # ____________________________________________


# user details override dj_rest_auth
class CustomeUserDetailsSerilizer(UserDetailsSerializer):
    class Meta:
        model = UserModel
        fields = ('email', 'username', 'name', 'bio', 'phone',
                  'facebook_link', 'github_link', 'instgram_link')


# password reset done by default
# you can make user logout when passowrd change


class CustomeUserResetPassword(PasswordResetSerializer):
    pass
