from django.urls import path
from . import views
from .views import *

urlpatterns = [
	path('', views.index , name = "homepage"),
    path('youtube-app/', views.youtube , name = "youtube"),
    path('weather-app/', views.weather,name="weather"),
    path('corona-app/', views.corona,name="corona"),
    path('delete/<city_name>/', views.delete_city, name='delete_city'),
 ]