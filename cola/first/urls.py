from django.urls import path
from . import views



urlpatterns = [
    path('',views.main, name="main"),
    path('board/',views.board, name="board"),
    path('board/<int:board_id>', views.detail, name="detail"),
    path('board/new/',views.new, name="new"),
    path('board/create', views.create, name="create"),

    #profile
    path('board/mypage/<str:username>/profileX',views.mypage, name="mypage_login"),
    path('board/mypage/<str:username>/XtoO',views.mypage, name="mypage"),
    path('board/mypage/profileO',views.mypage, name="mypage"),
    path('board/makeProf/',views.makeProfile, name="makeProfile"),
    path('board/makeProf/<int:profile>/<str:username>/',views.makeProfile, name="makeProfile"),
    path('board/changeProf/',views.makeProfile, name="changeProfile"),

    #logout
    path('board/logout/',views.logout, name="logout"),

    #path('board/mypage',views.mypage, name="mypage"),
    path('board/<int:board_id>/comment', views.add_comment_to_post, name='add_comment_to_post'),

] 