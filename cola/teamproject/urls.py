from django.urls import path
from . import views

urlpatterns = [
    path('teamproject/', views.teamproject, name="teamproject"),
    path('create', views.createTeam, name="createTeam"),
    path('teaminfo', views.teamInfo, name="teamInfo"),
    path('teaminfo/change', views.changeTeamInfo, name="changeTeamInfo"),
]