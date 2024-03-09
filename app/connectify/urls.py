from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls', namespace='base'), name='base'),
    path('blog/', include('blog.urls', namespace='blog'), name='blog'),
    path('account/', include('accounts.urls', namespace='accounts'), name='accounts'),
    path('user/', include('users.urls', namespace='users'), name='users'),
    path('room/', include('rooms.urls', namespace='rooms'), name='rooms'),
    path('api/', include('api.urls', namespace='api'), name='api'),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
