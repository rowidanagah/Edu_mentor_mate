from reactions.models import Likes
from blogs.api.serializers import BlogModelSerializer, BlogViewModelSerializer
from blogs.models import BLog
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


from tags.models import Category, Tags
from blogs.models import BLog
# =============================(list)====================================

from django.db.models import Q

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class createBlog(CreateAPIView):
    serializer_class = BlogModelSerializer
    queryset = BLog.objects.all()

class MyPagination(PageNumberPagination):
    page_size = 2  # number of items per page
    page_size_query_param = 'page_size'  # query parameter for page size
    max_page_size = 100  # maximum page size


class bloglist(ListAPIView):
    serializer_class = BlogViewModelSerializer
    #pagination_class = MyPagination
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

        # queryset = queryset.annotate(
        #         liked_by_user=Exists(
        #             Likes.objects.filter(user=user, blog=OuterRef('pk'), liked=True)
        #         )
        #     )

        # using query params
        blog_search_term = self.request.query_params.get(
            'title')
        print('------------------search-------------', blog_search_term)
        if blog_search_term:
            queryset = queryset.filter(Q(title__icontains=blog_search_term) | Q(
                content__icontains=blog_search_term))
            
        #paginated_queryset = MyPagination().paginate_queryset(queryset)
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
