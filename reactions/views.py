from django.shortcuts import render
from rest_framework.views import APIView
from blogs.models import BLog
from reactions.models import Likes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from .serializers import LikeSerializer
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
        blog, user = request.data['blog'], request.user
        print('----------req data-----------', blog)

        if not blog:
            return Response({'error': 'Missing blog_id parameter'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            blog = Likes.get_user_reaction_on_blog(blog=blog, user=user)
            print('----------req data-----------', blog)

        except BLog.DoesNotExist:
            return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

        like, created = Likes.objects.get_or_create(user=user, blog=blog)

        if not created:
            like.isLike = False
            return Response({'message': 'Like removed'}, status=status.HTTP_200_OK)
        like.isLike = True
        serializer = self.serializer_class(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
