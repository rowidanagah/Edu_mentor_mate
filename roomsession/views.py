from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import RoomSession
from .serializers import SessionSerializer , SessionViewSerializer
from rest_framework import status
# Create your views here.

from rest_framework.exceptions import NotFound
from .models import SessionDate, RoomSession
#################################### get whole sessions and post session ##########################################


@api_view(['GET', 'POST'])
def session_list(request):
    if request.method == 'GET':
        user = request.user
        favorite_tags = user.favourite_bins.all()
        print('----------------------USER-----------------------',
              favorite_tags)
        sessions = RoomSession.objects.filter(
            tags__in=favorite_tags).distinct().order_by('-updated_at')

        serializer = SessionViewSerializer(
            sessions, many=True , context={'request': request})
        return Response(serializer.data)

    if request.method == 'POST':
        
        serializer = SessionSerializer(data=request.data)
        if serializer.is_valid():
            room_session = serializer.save()

            data = request.data
            print("------available_dates-------------------------",
                  data['available_dates'])

            # for session_date in request.data.get('available_dates'):
            #     # try:
            #     #     session_date_obj = SessionDate.objects.get(
            #     #         id=session_date['id'])
            #     #     print("------------session_date_obj ------------------",
            #     #           session_date_obj)
            #     # except SessionDate.DoesNotExist:
            #     #     raise NotFound()
            #     session_date_obj, _ = SessionDate.objects.get_or_create(
            #         id=session_date['id'])
            #     room_session.available_dates.add(session_date_obj)

            room_session.save_session_available_dates(
                data['available_dates'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#################################### get specific session and delete specific session#############################


@api_view(['GET', 'Delete', 'PUT'])
def session_detail(request, pk):
    try:
        session = RoomSession.get_spesific_session_details(pk)
    except RoomSession.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SessionSerializer(session)
        return Response(serializer.data)

    if request.method == 'DELETE':
        session.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    if request.method == 'PUT':
        print("-------updating data------------")
        serializer = SessionSerializer(session, data=request.data)
        if serializer.is_valid(raise_exception=True):
            room_session, data = serializer.save(), request.data
            res = room_session.update_session_available_dates(
                data['available_dates'])
            print('ppppppppppppppppp', res)

            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_session(request, pk):
    print("-------updating data------------")
    try:
        session_details = RoomSession.get_spesific_session_details(pk)
    except RoomSession.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = SessionSerializer(session_details, data=request.data)
    if serializer.is_valid(raise_exception=True):
        room_session, data = serializer.save(), request.data
        room_session.update_session_available_dates(
            data['available_dates'])
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
