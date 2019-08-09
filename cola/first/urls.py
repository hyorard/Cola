from django.urls import path
from . import views



urlpatterns = [
    path('board/',views.board, name="board"),
    path('board/info',views.infoboard, name="infoboard"),
    path('board/info/searchPost',views.searchPost, name="searchPost"),
    path('board/<int:board_id>', views.detail, name="detail"),
    path('board/addComment', views.addComment, name='addComment'),
    path('board/deleteComment', views.deleteComment, name='deleteComment'),
    path('board/changeComment', views.changeComment, name='changeComment'),
    path('board/new/',views.new, name="new"),
    path('board/create2', views.create, name="create"),
    path('board/modify', views.modify, name="modify"),
    path('board/modify/<int:board_id>', views.modify, name="modify"),
    path('board/modifyAction', views.modifyAction, name="modifyAction"),
    path('board/modifyAction/<int:board_id>', views.modifyAction, name="modifyAction"),
    path('board/removeBoard/<int:board_id>', views.removeBoard, name="removeBoard"),

    #profile
    path('board/mypage/',views.mypage, name="mypage"),
    path('board/makeProf/',views.makeProfile, name="makeProfile"),
    path('board/changeProf/',views.changeProfile, name="changeProfile"),

    #logout
    path('board/logout/',views.logout, name="logout"),

    #path('board/mypage',views.mypage, name="mypage"),

] 