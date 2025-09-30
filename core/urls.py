from django.urls import path
from . import views
#サイト全体の共通ロジックを管理
urlpatterns = [
    path('', views.home, name='home'),
]
