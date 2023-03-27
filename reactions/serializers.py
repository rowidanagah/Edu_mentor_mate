from .models import Likes

from rest_framework import serializers


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = '__all__'
