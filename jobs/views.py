from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import GmailAccount
from .serializers import GmailAccountSerializer
from rest_framework.response import Response



# Create your views here.
@api_view(['GET', 'POST'])
def gmail_account_list(request):
    if request.method == 'GET':
        gmail_accounts = GmailAccount.objects.all()
        serializer = GmailAccountSerializer(gmail_accounts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = GmailAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)