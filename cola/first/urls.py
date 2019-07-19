from django.urls import path
from . import views



urlpatterns = [
    path('',views.main, name="main"),
    path('board/',views.board, name="board"),
    path('board/<int:board_id>', views.detail, name="detail"),
    path('board/new/',views.new, name="new"),
    path('board/create', views.create, name="create"),
    path('board/mypage',views.mypage, name="mypage"),
]