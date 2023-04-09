from django.shortcuts import get_object_or_404
from django.db import models
from tags.models import Tags
# from django.contrib.auth.models import User

from accounts.models import User
# Create your models here.

from django.utils import timezone

import datetime
from django.core.exceptions import ValidationError

# created_at = models.DateTimeField(default=datetime.datetime.now(), blank='true')


class SessionDate(models.Model):
    session_date = models.DateField(auto_now=False, unique=True)
    reserved = models.BooleanField(default=False)
    reserver = models.ForeignKey(
        User, null=True, blank=True, related_name='user_reserve', on_delete=models.SET_NULL)
    deruration = models.TimeField(
        auto_now=False, auto_now_add=False, null=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        print("-------datetime-------", timezone.now().date())
        print("-------datetime-------", self.session_date, self.deruration
              )
        if self.session_date < timezone.now().date():
            raise ValidationError("The date cannot be in the past!")
        super(SessionDate, self).save(*args, **kwargs)


ordering = ['1st', '2nd', '3rd', '4th',
            '5th', '6th', '7th', '8th', '9th', '10th']


class RoomSession(models.Model):
    title = models.CharField(max_length=100, null=False)
    tags = models.ManyToManyField(Tags, blank=True)
    mentor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='mentor_session')
    available_dates = models.ManyToManyField(SessionDate)
    sessionUrl = models.URLField(null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    # updated_at = models.DateField(auto_now=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    ended_at = models.DateField(auto_now=False)
    description = models.TextField(blank=False, null=False)
    # read_time=models.CharField(max_length=10, null=True)

    # user_bio = models.TextField(blank=True, null=True, editable=False)

    # def save(self, *args, **kwargs):
    #     self.user_bio = self.mentor.bio
    #     super(RoomSession, self).save(*args, **kwargs)

    @classmethod
    def get_sessions_details(cls):
        return cls.objects.all()

    @classmethod
    def get_spesific_session_details(cls, id):
        # return get_object_or_404(cls, pk=id)
        return cls.objects.get(id=id)

    def save_session_available_dates(self, available_dates, ended_at):
        for i, session_date in enumerate(available_dates):
            print("----------SESSION---------------------------------",
                  type(session_date['session_date']), session_date)

            try:
                # Parse the input string as a datetime object
                # date_obj = datetime.datetime.strptime(
                #     session_date['session_date'], '%Y-%m-%d').date()
                date_obj = datetime.datetime.strptime(
                    session_date['session_date'], "%Y-%m-%dT%H:%M").date()
            except ValueError:
                # Handle the case where the input string is not a valid date
                raise ValidationError('Invalid date')

            # date_obj = session_date['session_date']
            if ended_at < session_date['session_date']:

                raise ValidationError(
                    f'your {ordering[i]} session date exceeds your end date ')

            print("----------SESSION---------------------------------",
                  session_date['session_date'], session_date['deruration'])

            # get date object if exists yet create a new date object
            session_date_obj, _ = SessionDate.objects.get_or_create(
                session_date=date_obj)
            session_date_obj.reserved = session_date['reserved']
            session_date_obj.deruration = session_date['deruration']
            session_date_obj.price = session_date.get('price', 0)

            # session_date_obj, _ = SessionDate.objects.get_or_create(
            #     session_date=session_date['session_date']
            # )
            # session_date_obj.reserved = session_date['reserved']
            session_date_obj.save()
            self.available_dates.add(session_date_obj)

    def save_tags(self, tag_names):
        for tag_name in tag_names:
            tag, created = Tags.objects.get_or_create(caption=tag_name)
            self.tags.add(tag)

    @classmethod
    def get_mentor_number_of_sessions(cls, mentor):
        return cls.objects.filter(mentor=mentor).count()

    def update_session_available_dates(self, available_dates):
        updated_session_dates = []
        for session_date in available_dates:
            # try:
            #     # Parse the input string as a datetime object
            #     date_obj = datetime.datetime.strptime(
            #         session_date['session_date'], '%Y-%m-%d').date()
            # except ValueError:
            #     # Handle the case where the input string is not a valid date
            #     raise ValidationError('Invalid date')
            date_obj = session_date['session_date']
            print("----------SESSION---------------------------------",
                  type(session_date['session_date']), session_date)

            # get date object if exists yet create a new date object
            session_date_obj, _ = SessionDate.objects.get_or_create(
                session_date=date_obj)
            session_date_obj.reserved = session_date['reserved']
            if 'reserver' in session_date:
                pick_user = User.objects.filter(
                    user_id=session_date['reserver']).first()
                session_date_obj.reserver = pick_user
                print('------------', session_date)
            # session_date_obj.reserver = session_date['reserver']
            session_date_obj.save()

            print("------------------------", session_date)
            print("---------obj---------------", session_date['reserved'])
            print(session_date_obj)

            updated_session_dates.append(session_date_obj)
        print(self.available_dates)
        self.title = "title"
        self.available_dates.set(updated_session_dates)
        return updated_session_dates
