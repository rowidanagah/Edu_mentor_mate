from django.shortcuts import get_object_or_404
from django.db import models
from tags.models import Tags
from django.contrib.auth.models import User
# Create your models here.

from django.utils import timezone

import datetime
from django.core.exceptions import ValidationError

# created_at = models.DateTimeField(default=datetime.datetime.now(), blank='true')


class SessionDate(models.Model):
    datetime = models.DateField(auto_now=False, unique=True)
    reserved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        print("-------datetime-------", timezone.now().date())
        print("-------datetime-------", self.datetime)
        if self.datetime < timezone.now().date():

            raise ValidationError("The date cannot be in the past!")
        super(SessionDate, self).save(*args, **kwargs)


class RoomSession(models.Model):
    title = models.CharField(max_length=100, null=False)
    tags = models.ManyToManyField(Tags, blank=True)
    mentor = models.ForeignKey(User, on_delete=models.CASCADE)
    deruration = models.TimeField(auto_now=False, auto_now_add=False)
    available_dates = models.ManyToManyField(SessionDate)
    sessionUrl = models.URLField(null=False)
    # created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateField(auto_now=True, null=True, blank=True)
    ended_at = models.DateField(auto_now=False)

    @classmethod
    def get_sessions_details(cls):
        return cls.objects.all()

    @classmethod
    def get_spesific_session_details(cls, id):
        # return get_object_or_404(cls, pk=id)
        return cls.objects.get(id=id)

    def save_session_available_dates(self, available_dates):
        for session_date in available_dates:
            session_date_obj, _ = SessionDate.objects.get_or_create(
                id=session_date['id'])
            self.available_dates.add(session_date_obj)

    def update_session_available_dates(self, available_dates):
        updated_session_dates = []
        for session_date in available_dates:
            session_date_obj, _ = SessionDate.objects.get_or_create(
                id=session_date['id'])
            print("------------------------", session_date)
            print("---------obj---------------", session_date['reserved'])
            print(session_date_obj)

            updated_session_dates.append(session_date_obj)
        print(self.available_dates)
        self.title = "title"
        self.available_dates.set(updated_session_dates)
        return updated_session_dates
