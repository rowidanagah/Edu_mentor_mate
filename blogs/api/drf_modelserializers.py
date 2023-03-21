from blogs.api.serializers import BlogModelSerializer
from blogs.models import BLog
from rest_framework.generics import ListCreateAPIView ,RetrieveUpdateDestroyAPIView

# =============================(list)====================================
class bloglist(ListCreateAPIView):
    serializer_class = BlogModelSerializer
    queryset = BLog.objects.all()

# =============================(RetrieveUpdateDestroyAPIView)============
class BlogRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = BlogModelSerializer
    queryset = BLog.objects.all()
