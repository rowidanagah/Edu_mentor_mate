from django.db import models
from django.shortcuts import get_object_or_404
from markdownfield.models import MarkdownField, RenderedMarkdownField
from markdownfield.validators import VALIDATOR_STANDARD
# Create your models here.

from tags.models import Tags
from accounts.models import User, Mentor
from roomsession.models import RoomSession


class BLog(models.Model):
    title = models.CharField(max_length=100)
    # bookmark related stuff
    content = MarkdownField(rendered_field='text_rendered',
                            validator=VALIDATOR_STANDARD)

    text_rendered = RenderedMarkdownField()
    mentor = models.ForeignKey(User, on_delete=models.CASCADE)

    cover_image = models.ImageField(
        upload_to='images/blogs/', null=True, blank=True)
    tags = models.ManyToManyField(Tags, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    session = models.ForeignKey(
        RoomSession, related_name="bolg_avaliable_session", null=True, blank=True, on_delete=models.SET_NULL)

    @classmethod
    def get_blogs(cls):
        return cls.objects.all()

    @classmethod
    def get_spesific_blog(cls, blog_id):
        return cls.objects.get_object_or_404(blog_id)

    # def blog_has_session(self,blog):
    #     return blog.
