from blogs.api.serializers import BlogModelSerializer
from blogs.models import BLog
from rest_framework.generics import ListCreateAPIView ,RetrieveUpdateDestroyAPIView
from rest_framework.filters import  SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
# =============================(list)====================================
class bloglist(ListCreateAPIView):
    serializer_class = BlogModelSerializer
    queryset = BLog.objects.all()
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_fields = ['title']
    search_fields = ['title']

# =============================(RetrieveUpdateDestroyAPIView)============
class BlogRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = BlogModelSerializer
    queryset = BLog.objects.all()

# =============================(Filter )=================================
