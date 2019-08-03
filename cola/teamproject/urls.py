from django.urls import path
from . import views

urlpatterns = [
    path('teamproject/', views.teamproject, name="teamproject"),
    path('create', views.createTeam, name="createTeam"),
    path('teaminfo', views.teamInfo, name="teamInfo"),
    path('teaminfo/change', views.changeTeamInfo, name="changeTeamInfo"),
    path('teaminfo/createTodo', views.createTodo, name="createTodo"),
    path('teaminfo/deleteTodo', views.deleteTodo, name="deleteTodo"),
    path('teaminfo/changeTodo', views.changeTodo, name="changeTodo"),
    path('teaminfo/finishTodo', views.finishTodo, name="finishTodo"),
    path('searchPerson/<int:team_id>', views.searchPerson, name="searchPerson"),
    path('searchPerson/', views.searchPerson, name="searchPerson"),
    path('teamBoard/', views.teamBoard, name="teamBoard"),
    path('teamBoard/<int:teamBoard_id>', views.teamBoard, name="teamBoard"),
]