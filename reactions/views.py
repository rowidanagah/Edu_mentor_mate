from rest_framework.generics import ListAPIView, CreateAPIView
from .models import SessionFeedback
from .serializers import SessionFeedbackCReateSerializer, SessionFeedbackSerializer
from rest_framework import serializers
from accounts.models import User
from django.shortcuts import render
from rest_framework.views import APIView
from blogs.models import BLog
from reactions.models import Likes, Follow
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from .serializers import LikeSerializer, followSerializer, SessionFeedbackCReateSerializer
# Create your views here.


class LikeView(APIView):
    # permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, blog_id):
        blog = BLog.get_spesific_blog(blog_id)
        print("--------------USER----------------", request.user)
        user_reaction = Likes.get_user_reaction_on_blog(
            blog=blog, user=request.user)

        print("--------------USER REACTION----------------", request.user)

        return Response({"created": "success"})


class LikeAPIView(APIView):
    serializer_class = LikeSerializer
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        print('-------------------DATA', request.data)
        blog_id, user_id = request.data['blog'], request.data['user']
        if not blog_id:
            return Response({'error': 'Missing blog_id parameter'}, status=status.HTTP_400_BAD_REQUEST)
        if not user_id:
            return Response({'error': 'Missing user_id parameter'}, status=status.HTTP_400_BAD_REQUEST)

        blog = BLog.get_spesific_blog(blog_id)
        user = User.objects.filter(user_id=user_id).first()
        print('----------req data-----------', blog, user_id)

        like, created = Likes.objects.get_or_create(user=user, blog=blog)
        print('-----new ', created, like.isLike)
        like = Likes.toggle_like(like)
        serializer = self.serializer_class(like)
        print('----------------------res data', serializer.data)
        return Response({'message': 'Like added', "data": serializer.data}, status=status.HTTP_201_CREATED)


class followAPIView(APIView):
    serializer_class = followSerializer
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        print('-------------------DATA', request.data)
        mentor_id, user_id = request.data['following_mentor'], request.data['student']
        if not mentor_id:
            return Response({'error': 'Missing following_mentor_id parameter'}, status=status.HTTP_400_BAD_REQUEST)
        if not user_id:
            return Response({'error': 'Missing user_id parameter'}, status=status.HTTP_400_BAD_REQUEST)

        if user_id == mentor_id:
            raise serializers.ValidationError(
                "A user cannot follow themselves.")
        mentor = User.objects.filter(user_id=mentor_id).first()
        user = User.objects.filter(user_id=user_id).first()
        print('----------req data-----------', mentor, user)

        follow, created = Follow.objects.get_or_create(
            student=user, following_mentor=mentor)
        print('-----new ', created, follow.isfollow)
        follow = Follow.toggle_follow(follow)
        serializer = self.serializer_class(follow)
        print('----------------------res data', serializer.data)
        return Response({'message': 'follow added', "data": serializer.data}, status=status.HTTP_201_CREATED)


class SessionFeedbackAPIView(ListAPIView):
    queryset = SessionFeedback.objects.all()
    serializer_class = SessionFeedbackSerializer


class SessionFeedbackCreateApi(CreateAPIView):
    queryset = SessionFeedback.objects.all()
    serializer_class = SessionFeedbackCReateSerializer


class SessionFeedbackList(ListAPIView):
    queryset = SessionFeedback.objects.all()
    serializer_class = SessionFeedbackSerializer()

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context[] = 'Some extra data'
    #     return context


# class SessionFeedbackCreate(CreateAPIView):
#     serializer_class = SessionFeedbackCReateSerializer
