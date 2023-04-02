from django.urls import path
from roomsession.views import *

urlpatterns = [
    path('',session_list),
    path('<int:pk>', session_detail),
    path('api/gmail-accounts/', gmail_account_list, name='gmail-account-list'),
] 