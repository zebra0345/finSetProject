from django.contrib import admin
from django.urls import path, include
from . import views
app_name = 'chatBots'
urlpatterns = [
    path('', views.chatBot)
]
