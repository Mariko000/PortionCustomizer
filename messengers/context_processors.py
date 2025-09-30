# messengers/context_processors.py
#header.html のベルアイコンに「全体未読件数」を表示
from .models import Message

def unread_messages(request):
    if request.user.is_authenticated:
        count = Message.objects.filter(receiver=request.user, is_read=False).count()
        return {"unread_total": count}
    return {}

#Django のアプリロードが終わってから Message を参照する