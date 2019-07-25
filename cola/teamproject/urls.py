from django.urls import path
from . import views

urlpatterns = [
    path('teampage/',views.teamPage, name="teampage"), 
    path('teampage/create',views.createTeam, name="createTeam"),
]