from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index , name = "homepage"),
    path('weather-app/', views.weather,name="weather"),
    path('delete/<city_name>/', views.delete_city, name='delete_city'),
 ]