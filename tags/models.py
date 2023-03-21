from django.db import models

# Create your models here.

from django.shortcuts import get_object_or_404


class Tags(models.Model):
    caption = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return f"{self.caption}"

    @classmethod
    def get_spesific_tag(cls, caption):
        return cls.objects.filter(caption=caption)


class Specialization(models.Model):
    major = models.CharField(null=False, blank=False, max_length=50)
    DEGREES_TYPE_CHOICES = [
        ("bachelor", "Bachelor"),
        ("master", "Master")
    ]
    degree = models.CharField(max_length=10, null=True, blank=True,
                              choices=DEGREES_TYPE_CHOICES)

# could be a list&array of  charfield

class Tools(models.Model):
    name = models.CharField(max_length=10, blank=False,
                            null=False, primary_key=True)
