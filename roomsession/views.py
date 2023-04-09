from django.core.exceptions import ValidationError
from django.db.models import Q
from rest_framework import generics
from .serializers import UserPickedSessions
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import RoomSession
from .serializers import SessionSerializer, SessionViewSerializer, singleDateSerilizer
from rest_framework import status
# Create your views here.
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.exceptions import NotFound
from .models import SessionDate, RoomSession
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

#################################### get whole sessions and post session ##########################################

from django.urls import reverse


def update_user_fav_bins(instance, user):
    tags = instance.tags.all()

    user.favourite_bins.add(*tags)
    user.save()
    print('----------------------USER tags-----------------------',
          tags, user.favourite_bins)


@api_view(['GET', 'POST'])
def session_list(request):
    if request.method == 'GET':
        session_search_term = request.query_params.get('title')
        if session_search_term:
            sets = RoomSession.objects.all()
            search_session = sets.filter(Q(title__icontains=session_search_term) | Q(
                description__icontains=session_search_term))
            sessions = SessionViewSerializer(
                search_session,  many=True, context={'request': request})
            return Response(sessions.data)

        user = request.user
        favorite_tags = user.favourite_bins.all()
        print('----------------------USER-----------------------',
              favorite_tags)
        sessions = RoomSession.objects.filter(
            tags__in=favorite_tags).distinct().order_by('-created_at')

        serializer = SessionViewSerializer(
            sessions, many=True, context={'request': request})

        return Response(serializer.data)

    if request.method == 'POST':
        if 'tags' in request.data:
            tags_name = request.data.pop('tags')

        print('---------data', request.data)
        serializer = SessionSerializer(data=request.data)
        if serializer.is_valid():
            print('-------ment', request.data['mentor'])
            room_session = serializer.save()

            data = request.data
            if not data['available_dates']:
                room_session.delete()
                return Response({"available_dates": "You can't"}, status=status.HTTP_400_BAD_REQUEST)

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
            end_date = request.data['ended_at']
            try:
                room_session.save_session_available_dates(
                    data['available_dates'], end_date)
            except ValidationError as e:
                room_session.delete()
                return Response({"exceeds_end_date": e.message}, status=status.HTTP_400_BAD_REQUEST)

            print('------------------tgas', tags_name)
            room_session.save_tags(tags_name)
            update_user_fav_bins(room_session, request.user)

            # session_url = reverse('session-detail', args=[serializer.da.id])

            # data = {
            #     request.data,
            #     'url': request.build_absolute_uri(session_url),

            # }
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
        serializer = SessionViewSerializer(
            session, context={'request': request})
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


class SingleDateRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = SessionDate
    queryset = SessionDate.objects.all()


class singleDateUpdateView(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def patch(self, request, *args, **kwargs):
        pk = kwargs['pk']
        user = request.user
        print("_________________________helo")

        session = SessionDate.objects.get(id=pk)
        session.reserver = request.user
        print("session______", session.reserver)
        serializer = singleDateSerilizer(
            session, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        """
        `Update single date`
        """
        # user = self.request.user
        # serializer = singleDateSerilizer(user, data=request.data, partial=True)

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']

        session = SessionDate.objects.get(id=pk)
        serializer = singleDateSerilizer(session)
        print(session)
        return Response(serializer.data)


class UserPickedSessionsView(generics.ListAPIView):
    serializer_class = UserPickedSessions

    def get_queryset(self):
        user = self.request.user
        result = SessionDate.objects.filter(reserver=user, reserved=True)
        # result = RoomSession.objects.filter(available_dates__reserved=True)
        # print(result)
        return result

# mintor picked sessions
# get availables dates created by mentor and reserved


class MintorPickedSessionsView(generics.ListAPIView):
    serializer_class = UserPickedSessions

    def get_queryset(self):
        user = self.request.user
        result = SessionDate.objects.filter(
            roomsession__mentor=user, reserved=True)
        return result
