from django.shortcuts import render

# Create your views here.
from .models import User
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import SessionAuthentication ,TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer ,UserUpdateSerializer
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

from rest_framework import permissions, status
from .validations import custom_validation, validate_email, validate_password
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.registration.views import VerifyEmailView
from django.utils.translation import gettext_lazy as _



class UserRegister(APIView):
	permission_classes = (permissions.AllowAny,)
	def post(self, request):
		clean_data = custom_validation(request.data)
		serializer = UserRegisterSerializer(data=clean_data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.create(clean_data)
			if user:
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = (SessionAuthentication,)
	##
	def post(self, request):
		data = request.data
		# assert validate_email(data)
		# assert validate_password(data)
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.check_user(data)
			data={ 'message':"login succefully", 'token':user.auth_token.key  }
			login(request, user)
			return Response(data, status=status.HTTP_200_OK)


class UserLogout(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,TokenAuthentication)
	def post(self, request):
		request.user.auth_token.delete()
		logout(request)

		return Response(status=status.HTTP_200_OK)


class UserView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,TokenAuthentication)
	##
	def get(self, request):
		serializer = UserSerializer(request.user)
		return Response({'user': serializer.data}, status=status.HTTP_200_OK)

  


class UpdateUser(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    def patch(self, request):
        """
        `Update User`
        """
        user = self.request.user
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    

@api_view(['GET'])
def get_specific_user(request, pk):
    try:
        user = User.objects.get(user_id=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)





