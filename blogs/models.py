from django.db import models
from django.shortcuts import get_object_or_404
# Create your models here.

from tags.models import Tags
from django.contrib.auth.models import User
from roomsession.models import RoomSession

from accounts.models import User
from tags.models import Category


class BLog(models.Model):
    title = models.CharField(max_length=100)
    # bookmark related stuff
    content = models.TextField(blank=False, null=False)

    mentor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='mentor_blog')

    cover_image = models.ImageField(
        upload_to='images/blogs/', null=True, blank=True)
    tags = models.ManyToManyField(Tags, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    session = models.ForeignKey(
        RoomSession, related_name="bolg_avaliable_session", null=True, blank=True, on_delete=models.SET_NULL)

    # category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True,
    #                              related_name='blog_category', blank=True)

    @classmethod
    def get_blogs(cls):
        return cls.objects.all()

    def __str__(self):
        return self.title

    @classmethod
    def get_spesific_blog(cls, blog_id):
        return get_object_or_404(cls, pk=blog_id)

    @classmethod
    def get_blog_by_title(cls, title):
        return cls.objects.filter(title__contains=title)

    @classmethod
    def get_mentor_number_of_blogs(cls, mentor):
        return cls.objects.filter(mentor=mentor).count()

    # def blog_has_session(self,blog):
    #     return blog.
