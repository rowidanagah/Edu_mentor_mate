from django.urls import path
from .views import LikeAPIView

from roomsession.views import session_list
urlpatterns = [
    path('like/', LikeAPIView.as_view(), name='like'),

]
