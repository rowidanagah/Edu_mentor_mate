from django.db import models
from tags.models import Tags
from accounts.models import User
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
