from django.contrib import admin
from django.urls import path, include
from . import views
app_name = 'finSetApp'
urlpatterns = [
    # 예금데이터 전체 생성
    path('depositProductsCreate/', views.depositDataCreated),
    # 적금데이터 전체생성
    path('savingProductsCrate/', views.savingsDataCreate),

    # 예금데이터 전체 조회
    path('depositProductsAll/', views.depositProductsAll),
    # 예금데이터 상세 조회
    path('depositProduct/<int:pk>/', views.depositProductDetail),
    # 해당 예금데이터의 옵션조회
    path('depositOptions/<int:pk>/', views.depositProductOptions),
    # 예금 옵션데이터 조회와 수정
    path('depositOptionDetail/<int:pk>/', views.optionDetail),
    

    # 적금데이터 전체조회
    path('SavingProductsAll/', views.SavingProductsAll),
    # 적금데이터 상세 조회
    path('SavingProduct/<int:pk>/', views.SavingProductOptions),
    # 해당 적금데이터의 옵션조회
    path('SavingOptions/<int:pk>/', views.optionDetail),
]
