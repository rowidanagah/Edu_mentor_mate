from django.contrib import admin

# Register your models here.
from .models import GmailAccount

admin.site.register(GmailAccount)