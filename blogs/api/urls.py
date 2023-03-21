from django.urls import path
from blogs.api.drf_modelserializers import *

urlpatterns = [
    path('blogsapi/', bloglist.as_view(), name='blogs'),
    path('blogsapi/<int:pk>',BlogRetrieveUpdateDestroyAPIView.as_view(), name='blogsupdate'),
]