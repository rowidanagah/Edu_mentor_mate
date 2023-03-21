from django.contrib import admin

# Register your models here.
from roomsession.models import SessionDate, RoomSession


admin.site.register(SessionDate)
admin.site.register(RoomSession)
