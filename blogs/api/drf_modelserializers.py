from blogs.api.serializers import BlogModelSerializer , BlogViewModelSerializer
from blogs.models import BLog
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView , ListAPIView , CreateAPIView
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


from tags.models import Category, Tags
from blogs.models import BLog
# =============================(list)====================================

from django.db.models import Q


class createBlog(CreateAPIView):
    serializer_class = BlogModelSerializer
    queryset = BLog.objects.all()
   

class bloglist(ListAPIView):
    serializer_class = BlogModelSerializer
    # queryset = BLog.objects.all()
    # filter_backends = [DjangoFilterBackend,SearchFilter]
    # filterset_fields = ['title']
    # search_fields = ['title']

    def get_queryset(self):
        user = self.request.user
        # Get user's favorite tags
        favorite_tags = user.favourite_bins.all()
        print('----------------------USER-----------------------',
              favorite_tags)
        # blog_categories = [c.name for c in categories]
        # queryset = BLog.objects.filter(category__in=blog_categories)

        # Using `distinct()` to avoid duplicate blogs
        queryset = BLog.objects.filter(
            tags__in=favorite_tags).distinct().order_by('-updated_at')

        print("-------------------session blog-----------------------",
              queryset)
        # using query params
        blog_search_term = self.request.query_params.get(
            'title')
        if blog_search_term:
            BLog.objects.filter(Q(title__icontains=blog_search_term) | Q(
                content__icontains=blog_search_term))
        return queryset


# class BlogListView(generics.ListAPIView):
#     serializer_class = BlogSerializer

#     def get_queryset(self):
#         user = self.request.user
#         categories = Category.objects.filter(user=user)
#         blog_categories = [c.name for c in categories]
#         queryset = Blog.objects.filter(category__in=blog_categories)
#         return queryset


# =============================(RetrieveUpdateDestroyAPIView)============
class BlogRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = BlogModelSerializer
    queryset = BLog.objects.all()

# =============================(Filter )=================================
