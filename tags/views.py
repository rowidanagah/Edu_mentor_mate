from django.shortcuts import render
from tags.models import Tags
from tags.serializers import TagSerializer
from rest_framework.generics import ListAPIView
# Create your views here.



class tagslist(ListAPIView):
    serializer_class = TagSerializer
    queryset = Tags.objects.all()