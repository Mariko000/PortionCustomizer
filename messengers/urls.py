from django.urls import path
from . import views

app_name = "messengers"

urlpatterns = [
    path("inbox/", views.inbox, name="inbox"),
    path("conversation/<int:user_id>/", views.conversation, name="conversation"),
]
