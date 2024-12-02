from django.contrib import admin
from django.urls import path, include
from . import views
app_name = 'accounts'
urlpatterns = [
    # 로그아웃 auth/logout/ - POST 로 로그아웃 기능 가능
    # auth/user/ - GET 방식으로 유저 객체 자체 반환
    # auth/user/에는 헤더에 토큰을 넘겨줘야함
    path('auth/', include('dj_rest_auth.urls')),
    #회원가입
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('account/', include('allauth.urls')),
    # 프로필 조회
    path('profile/<int:user_pk>/', views.profile),
    # 예금 추가하기
    path('deposit/<int:profile_pk>/<int:deposit_pk>/', views.profile_add_deposit),
    # 적금 추가하기
    path('saving/<int:profile_pk>/<int:saving_pk>/', views.profile_add_saving),
    # 회원탈퇴
    path('delete_user/', views.delete_user)
]
