from django.urls import path
from . import views

urlpatterns = [
    path('teamproject/',views.teamproject, name="teamproject"),
    path('/teaminfo',views.teamInfo, name="teamInfo"), 
    path('teampage/create',views.createTeam, name="createTeam"),
]