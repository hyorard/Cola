from django.urls import path
from . import views

urlpatterns = [
    path('teamproject/', views.teamproject, name="teamproject"),
    path('create', views.createTeam, name="createTeam"),
    path('teaminfo', views.teamInfo, name="teamInfo"),
    path('teaminfo/change', views.changeTeamInfo, name="changeTeamInfo"),
    path('searchPerson/<int:team_id>', views.searchPerson, name="searchPerson"),
    path('searchPerson/', views.searchPerson, name="searchPerson"),
]