from django.urls import path
from . import views

urlpatterns = [
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
    path('teamBoard/<int:team_id>', views.teamBoard, name="teamBoard"),
    path('teamboard_new/<int:team_id>', views.teamboard_new, name="teamboard_new"),
    path('teamboard_write/<int:team_id>', views.teamboard_write, name="teamboard_write"),
    path('teamBoard/detail/<int:board_id>', views.teamdetail, name="teamdetail"),
    path('board/removeBoardTb/<int:board_id>', views.removeBoardTb, name="removeBoardTb"),
    path('board/modifyTb', views.modifyTb, name="modifyTb"),
    path('board/modify/<int:board_id>', views.modifyTb, name="modifyTb"),
    path('board/modifyActionTb', views.modifyActionTb, name="modifyActionTb"),
    path('board/modifyActionTb/<int:board_id>', views.modifyActionTb, name="modifyActionTb"),
    path('teamBoard/detail/addcomment', views.addCommentTb, name="addCommentTb"),
    path('teamBoard/detail/deletecomment', views.deleteCommentTb, name="deleteCommentTb"),
    path('teamBoard/detail/changecomment', views.changeCommentTb, name="changeCommentTb"),
]