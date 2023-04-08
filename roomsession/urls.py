from django.urls import path
from roomsession.views import *

urlpatterns = [
    path('', session_list),
    path('<int:pk>', session_detail),
    path('session-date/<int:pk>', singleDateUpdateView.as_view()),
    path('user_picked_sessions/', UserPickedSessionsView.as_view(),
         name='picked-session-list'),
    path('mintor_picked_session-list/',MintorPickedSessionsView.as_view())

]
