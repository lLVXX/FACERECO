from django.urls import path
from . import views

urlpatterns = [
    path('video_feed/', views.video_feed, name='video_feed'),

    
    path('', views.stream_page, name='stream_page'),
]
