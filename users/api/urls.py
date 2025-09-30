#users/api/urls.py
from django.urls import path
from .. import views
from ..views import UserListView, login_history_api

app_name = 'users_api'

urlpatterns = [
    path('current-user/', views.current_user_info, name='current_user_info'),
    path('list/', UserListView.as_view(), name='user_list'),
    path('history/', login_history_api, name='history'),
]
