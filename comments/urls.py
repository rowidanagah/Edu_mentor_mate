

from django.urls import path, include

from .views import *
urlpatterns = [

    path('comments/', CommentList.as_view()),
    path('comments/<int:pk>/', CommentDetail.as_view()),
]
