
from django.urls import path, include

from tags.views import tagslist

urlpatterns = [
    path('api/tags/', tagslist.as_view(), name='tags'), 
]