from rest_framework import serializers
from roomsession.models import RoomSession,SessionDate



class SessionDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionDate
        fields = '__all__'

class SessionSerializer(serializers.ModelSerializer):
    available_dates = SessionDateSerializer(many=True)
    
    class Meta:
        model = RoomSession
        fields = '__all__'