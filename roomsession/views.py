from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import RoomSession
from .serializers import SessionSerializer
from rest_framework import status
# Create your views here.

from rest_framework.exceptions import NotFound
from .models import SessionDate, RoomSession
#################################### get whole sessions and post session ##########################################


@api_view(['GET', 'POST'])
def session_list(request):
    if request.method == 'GET':
        sessions = RoomSession.objects.all()
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = SessionSerializer(data=request.data)
        if serializer.is_valid():
            room_session = serializer.save()

            data = request.data
            print("------available_dates-------------------------",
                  data['available_dates'])

            for session_date in request.data.get('available_dates'):
                try:
                    session_date_obj = SessionDate.objects.get(
                        id=session_date['id'])
                    print("------------session_date_obj ------------------",
                          session_date_obj)
                    room_session.available_dates.add(session_date_obj)
                except SessionDate.DoesNotExist:
                    raise NotFound()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#################################### get specific session and delete specific session#############################


@api_view(['GET', 'Delete'])
def session_detail(request, pk):
    try:
        session = RoomSession.objects.get(id=pk)
    except RoomSession.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SessionSerializer(session)
        return Response(serializer.data)

    if request.method == 'DELETE':
        session.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
