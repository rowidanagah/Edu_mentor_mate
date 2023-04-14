from django.urls import path
from blogs.api.drf_modelserializers import *


urlpatterns = [
    path('blogsapi/', bloglist.as_view(), name='blogs'),
    path('create_blog_api/', createBlog.as_view(), name='create_blog'),
    path('blogsapi/<int:pk>',
         BlogRetrieveUpdateDestroyAPIView.as_view(), name='blogsupdate'),
    path('mentoractivity/<int:pk>',
         UserActivityAPIView.as_view(), name='mentor_activity'),
    path('trends', blog_trends, name="blog_trends")
]
