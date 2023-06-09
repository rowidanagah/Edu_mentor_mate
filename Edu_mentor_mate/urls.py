"""Edu_mentor_mate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
# ==(osama)====
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('api/', include('accounts.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),

    path('admin/', admin.site.urls),
    path('roomsession/', include('roomsession.urls')),
    # ===(osama)===
    path('api-auth/', include('rest_framework.urls')),
    path('', include('blogs.urls')),
    path('', include('tags.urls')),
    path('', include('comments.urls')),
    path('', include('reactions.urls')),
    path('jobs/', include('jobs.urls')),

]
# ===(osama)===
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
