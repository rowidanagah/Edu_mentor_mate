from blogs.models import BLog
from rest_framework import serializers

class BlogModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BLog
        fields = '__all__'
