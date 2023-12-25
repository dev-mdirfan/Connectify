from django.urls import path
from . import views

urlpatterns = [
    path('profile/<int:pk>', views.profile, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('user/', views.user, name='user'),
    path('user/update/', views.user_update, name='user_update'),
    
]