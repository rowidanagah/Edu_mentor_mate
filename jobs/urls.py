from django.urls import path
from .views import *

urlpatterns = [
    path('api/gmail-accounts/', gmail_account_list, name='gmail-account-list'),
] 