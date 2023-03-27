from django.shortcuts import render
from rest_framework.views import APIView
from blogs.models import BLog
from reactions.models import Likes
from rest_framework.response import Response

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
