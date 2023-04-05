from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import RoomSession
from .serializers import SessionSerializer,singleDateSerilizer
from rest_framework import status
# Create your views here.
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication ,TokenAuthentication
from rest_framework.exceptions import NotFound
from .models import SessionDate, RoomSession
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

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

        serializer = SessionSerializer(
            sessions, many=True)
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


class SingleDateRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = SessionDate
    queryset = SessionDate.objects.all()




class singleDateUpdateView(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    authentication_classes = (SessionAuthentication,TokenAuthentication)
	
    def patch(self, request,*args, **kwargs):
        pk = kwargs['pk']

        session = SessionDate.objects.get(id=pk)
        serializer = singleDateSerilizer(session,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        """
        `Update single date`
        """
        # user = self.request.user
        # serializer = singleDateSerilizer(user, data=request.data, partial=True)
    def get(self  , request, *args, **kwargs):
            pk = kwargs['pk']

            session = SessionDate.objects.get(id=pk)
            serializer = singleDateSerilizer(session)
            print(session)
            return Response(serializer.data)
                
