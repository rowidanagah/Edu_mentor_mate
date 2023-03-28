

from django.urls import path, include

from .views import *
urlpatterns = [

    path('comments/', CommentList.as_view()),
    path('comments/<int:pk>/', CommentDetail.as_view()),
    path('blogs/<int:blog_id>/comments/',
         CommentListAPIView.as_view(), name='comment-list'),
]
