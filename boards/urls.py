from django.contrib import admin
from django.urls import path, include
from . import views
app_name = 'boards'
urlpatterns = [
    # 게시글 전체조회와 게시글 생성하기
    path('', views.boards),
    # 게시글 디테일(댓글도 같이 넘어옴), 댓글 생성하기
    path('<int:pk>/', views.boards_detail),
    path('comment/<int:pk>/', views.comment_delete)
]
