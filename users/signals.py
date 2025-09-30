from django.dispatch import receiver
from allauth.account.signals import user_logged_in
from .models import LoginHistory
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from .views import update_login_streak


@receiver(user_logged_in)
def create_login_history(request, user, **kwargs):
    """
    ユーザーがログインしたときにログイン履歴を記録します。
    """
    LoginHistory.objects.get_or_create(user=user, login_date=datetime.date.today())

def handle_user_login(sender, request, user, **kwargs):
    """
    ユーザーがログインするたびに 連続日数 & レベル が自動更新   
    """
    update_login_streak(user)



