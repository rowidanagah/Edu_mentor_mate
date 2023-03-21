from django.contrib import admin

# Register your models here.


from tags.models import *

admin.site.register(Tags)
admin.site.register(Specialization)

admin.site.register(Tools)
