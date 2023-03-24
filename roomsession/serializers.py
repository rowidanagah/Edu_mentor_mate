from rest_framework import serializers
from roomsession.models import RoomSession, SessionDate


class SessionDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionDate
        fields = '__all__'


class SessionSerializer(serializers.ModelSerializer):
    available_dates = SessionDateSerializer(many=True, read_only=True)

    class Meta:
        model = RoomSession
        fields = ('title', 'available_dates', 'mentor',
                  'ended_at', 'sessionUrl', 'tags', 'deruration')
        #depth = 1

    # def create(self, validated_data):
    #     print("-------------validation------", validated_data)
    #     dates = validated_data.pop("available_dates")
    #     print("-------------------pop----------------", dates)
    #     session_rom = RoomSession.objects.create(**validated_data)
    #     return session_rom
