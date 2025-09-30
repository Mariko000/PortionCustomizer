from django.urls import path
from .views import search_view

app_name = 'search'

urlpatterns = [
    path('', search_view, name='search_view'),  # /search/ にアクセスすると search_view が呼ばれる
]
