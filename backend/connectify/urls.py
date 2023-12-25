"""
URL configuration for connectify project.

This file contains the URL configuration for the connectify project. It defines the URL patterns for the different views and endpoints of the project.

The urlpatterns list is used to define the URL patterns. Currently, it only includes the path for the admin site.

If the DEBUG setting is enabled, additional URL patterns are added for serving static and media files using the static() function from django.conf.urls.static module.

"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('pages.urls')),
    path('', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
