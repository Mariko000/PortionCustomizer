from django.urls import path
from .views import FollowAPIView, UnfollowAPIView, BlockAPIView, UnblockAPIView

app_name = "followers"

# followers/urls.py
urlpatterns = [
    path("follow/<int:user_id>/", FollowAPIView.as_view(), name="follow_api"),
    path("unfollow/<int:user_id>/", UnfollowAPIView.as_view(), name="unfollow"),
    path("block/<int:user_id>/", BlockAPIView.as_view(), name="block_user"),
    path("unblock/<int:user_id>/", UnblockAPIView.as_view(), name="unblock_user"),
]
