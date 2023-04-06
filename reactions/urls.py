from django.urls import path
from .views import LikeAPIView, followAPIView, SessionFeedbackAPIView, SessionFeedbackCreateApi

from roomsession.views import session_list
urlpatterns = [
    path('like/', LikeAPIView.as_view(), name='like'),
    path('follow/', followAPIView.as_view(), name='like'),
    path('SessionFeedback/', SessionFeedbackAPIView.as_view(), name='blog-list'),
    path('SessionFeedback/create/',
         SessionFeedbackCreateApi.as_view(), name='blog-create'),

]
