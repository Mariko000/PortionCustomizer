from django.urls import path
from django.urls import re_path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    # いいね機能のURL
    path('post/<int:pk>/like/', views.post_like, name='post_like'), 
    # エクササイズの投稿ができる機能のURLを追加
    path('exercise-log/', views.exercise_log_list, name='exercise_log_list'),
    # チェックボックスで選択されたものを削除
    path('delete-selected/', views.delete_selected_posts, name='delete_selected_posts'),
    # 全部削除
    path('posts/delete_all/', views.delete_all_posts, name='delete_all_posts'),
    # pk と slug の両方を必須で受け取る
    # 新：Unicode slug に対応　日本語もマッチ・\w = [a-zA-Z0-9_]・ぁ-ん = ひらがな・ァ-ン = カタカナ・一-龥 = 漢字
    re_path(r'^post/(?P<pk>[0-9]+)/(?P<slug>[-\wぁ-んァ-ン一-龥]+)/$', views.post_detail, name='post_detail'),


]