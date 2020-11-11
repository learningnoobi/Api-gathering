from django.urls import path
from . import views
from .views import *

urlpatterns = [
	path('', views.index , name = "homepage"),
    path('youtube-app/', views.youtube , name = "youtube"),
   path('corona-app/', views.corona,name="corona"),

 ]