from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, GenericAPIView
from .models import Comment
from .serializer import CommentSerializer,CommentPostSerializer
# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

# ================ Handle Comment Section ============

class CommentList(ListCreateAPIView):
    queryset = Comment.objects.all()
    # serializer_class = CommentPostSerializer
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentSerializer
        elif self.request.method == 'POST':
            return CommentPostSerializer


class CommentDetail(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def put(self, request, *args, **kwargs):
        comment = self.get_object()
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentListAPIView(ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        # blog_id = self.kwargs['blog_id'] # send blog id in req url
        blog_id = self.request.query_params.get(
            'blog_id')  # using query params
        print('----------BLOG----------', blog_id)
        return Comment.objects.filter(blog=blog_id)
    


@api_view(['DELETE'])
def delete_specific_comment(request, pk):
    try:
        comment = Comment.objects.get(id=pk)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


