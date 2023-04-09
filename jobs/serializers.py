from rest_framework import serializers
from .models import GmailAccount

class GmailAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = GmailAccount
        fields = ['id', 'email']