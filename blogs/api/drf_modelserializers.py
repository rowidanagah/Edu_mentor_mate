from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from tags.models import Category, Tags
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from blogs.models import BLog
from blogs.api.serializers import BlogModelSerializer, BlogViewModelSerializer
from reactions.models import Likes
from rest_framework import status
from django.db.models import Count, Subquery, OuterRef


# =============================(list)====================================


class createBlog(CreateAPIView):
    serializer_class = BlogModelSerializer
    queryset = BLog.objects.all()

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)

    #     # Save new tags
    #     tag_names = request.data.getlist('tags')
    #     print('--------------------', tag_names)
    #     tags = [Tags.objects.get_or_create(caption=tag_name)[
    #         0] for tag_name in tag_names]

    #     self.perform_create(serializer, tags)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def perform_create(self, serializer, tags):
    #     serializer.save(tags=tags)

    # def create(self, request, *args, **kwargs):
    #     # Get the tags data from the request
    #     tags_data = request.data.pop('tags', [])
    #     print('-------------------------', tags_data)
    #     # Call the superclass create() method to create the blog object
    #     response = super().create(request, *args, **kwargs)

    #     # Create new tag objects for any new tag names
    #     # for tag_caption in tags_data:
    #     #     tag, created = Tags.objects.get_or_create(caption=tag_caption)
    #     #     if created:
    #     #         tag.save()

    #     #         # # Add the new or existing tag to the blog's tags
    #     #         # response.data['tags'].append(tag.id)
    #     #         # response.data['tags_detail'].append(
    #     #         #     {'id': tag.id, 'caption': tag.name})

    #     # # Return the response
    #     # return response


class MyPagination(PageNumberPagination):
    page_size = 2  # number of items per page
    page_size_query_param = 'page_size'  # query parameter for page size
    max_page_size = 100  # maximum page size


class bloglist(ListAPIView):
    serializer_class = BlogViewModelSerializer
    # pagination_class = MyPagination
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

        # using query params for trends
        blogs_trends = self.request.query_params.get(
            'trends')
        print('------------TRENDS-------', blogs_trends)
        print('------------------search-------------', blog_search_term)

        if blog_search_term:
            queryset = queryset.filter(Q(title__icontains=blog_search_term) | Q(
                content__icontains=blog_search_term))

        if blogs_trends:
            blog = BLog.objects.all()
            # blogs = BLog.objects.annotate(
            #     num_Likes=Count('blog_reaction')).order_by('-num_Likes')

            blogs_trend = BLog.objects.annotate(num_true_likes=Count('blog_reaction', filter=Q(
                blog_reaction__isLike=True))).order_by('-num_true_likes')[:6]

            # blogs_trend = BLog.objects.annotate(num_true_likes=Count(
            #     'blog_reaction')).order_by('-num_true_likes')

            return blogs_trend
        print('---------------out')
        # paginated_queryset = MyPagination().paginate_queryset(queryset)
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
    serializer_class = BlogViewModelSerializer
    queryset = BLog.objects.all()

# =============================(Filter )=================================
