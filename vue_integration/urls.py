# vue_integration/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.vue_index, name='vue_index'),
    #API エンドポイント
    path('api/current_user/', views.current_user, name='current_user'),
]
