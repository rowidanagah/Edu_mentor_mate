from tags.models import Tags, Specialization, Tools

from django.db import models

# Create your models here.

from django.core.validators import *

# Create your models here.


class User(models.Model):
    name = models.CharField(null=False, max_length=50)
    email = models.EmailField(null=False, max_length=254)
    password = models.CharField(null=False, max_length=50)
    confirm_password = models.CharField(null=False, max_length=50)
    bio = models.TextField(null=True, max_length=150, blank=True)
    USER_TYPE_CHOICES = [
        ("mentor", "Mentor"),
        ("student", "Student")
    ]
    usertype = models.CharField(max_length=2,
                                choices=USER_TYPE_CHOICES,
                                default="student")
    user_profile = models.ImageField(upload_to='images/', blank=True)
    phone_regex = RegexValidator(
        regex=r'^01[1|0|2|5][0-9]{8}$', message='phone must be an egyptian phone number...')
    phone = models.CharField(verbose_name="phone", null=True, validators=[
        phone_regex], max_length=14)
    date_birth = models.DateField(null=True)
    facebook_link = models.URLField(null=True)
    github_link = models.URLField(null=True)
    instgram_link = models.URLField(null=True)
    joinDate = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class Student(User):
    favourite_bins = models.ManyToManyField(Tags, blank=True)


class Mentor(User):
    specializations = models.ForeignKey(
        Specialization, related_name="mentor_specialization")  # major
    tools = models.ManyToManyField(
        Tools, related_name="mentor_tools", blank=True)
