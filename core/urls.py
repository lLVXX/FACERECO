from django.urls import path
from . import views

urlpatterns = [
    path('', views.elegir_clase, name='elegir_clase'),
    path('clase/<int:asignatura_id>/', views.clase_view, name='clase_view'),
    path('video_feed/', views.video_feed, name='video_feed'),
]
