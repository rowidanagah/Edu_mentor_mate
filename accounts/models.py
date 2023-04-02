from tags.models import Tags, Specialization, Tools

from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

# Create your models here.

from django.core.validators import *



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)

        user.set_password(password)

        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to have is_staff being True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_superuser being True")

        return self.create_user(email=email, password=password, **extra_fields)

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=50)
    # password = models.CharField(null=False, max_length=50)
    # confirm_password = models.CharField(null=False, max_length=50)
    bio = models.TextField(null=True, max_length=150, blank=True)
    USER_TYPE_CHOICES = [
      ("mentor", "Mentor"),
      ("student", "Student")
    ]
    usertype = models.CharField(max_length=10,
                                choices=USER_TYPE_CHOICES,
                                default="student")
    user_profile = models.ImageField(upload_to='images/accounts', blank=True)
    
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
    favourite_bins = models.ManyToManyField(Tags, blank=True,null=True)
    is_staff=models.BooleanField(default=True)
    specializations = models.ForeignKey(
        Specialization, related_name="mentor_specialization", null=True, blank=True, on_delete=models.SET_NULL)  # major
    tools = models.ManyToManyField(
        Tools, related_name="mentor_tools", blank=True , null=True)
    is_active=models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = CustomUserManager()
    def __str__(self):
		   return self.username


class StudentManger(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(usertype="student")


class MentorManger(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(usertype="mentor")
