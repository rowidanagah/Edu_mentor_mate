from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, GenericAPIView
from .models import Comment
from .serializer import CommentSerializer,CommentPostSerializer
# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.views.decorators.http import require_http_methods
import json
from django.http import JsonResponse
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
        serializer = CommentPostSerializer(comment, data=request.data)
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
    

# @require_http_methods(["DELETE"])
# def delete_specific_comment(request):
#     try:
#         data = json.loads(request.body)
#         comment_id = data.get('comment_id')
#         user_id = data.get('user_id')
#         comment = Comment.objects.filter(id=comment_id, user_id=user_id).first()
#         if comment:
#             comment.delete()
#             return JsonResponse({'success': True})
#         else:
#             return JsonResponse({'success': False, 'message': 'Comment not found or you are not authorized to delete it.'}, status=404)

#     except Exception as e:
#         return JsonResponse({'success': False, 'message': str(e)})
