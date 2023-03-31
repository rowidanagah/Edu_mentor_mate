from django.urls import path
from .views import LikeAPIView, followAPIView

from roomsession.views import session_list
urlpatterns = [
    path('like/', LikeAPIView.as_view(), name='like'),
    path('follow/', followAPIView.as_view(), name='like'),

]
