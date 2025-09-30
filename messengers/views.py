from django.contrib import messages
from profanity_filter.utils import check_for_profanity
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Count, Q

from followers.models import Follow
from .models import Message

User = get_user_model()

@login_required
def inbox(request):
    """
    ログインユーザーがフォローしているユーザー一覧を表示。
    かつ各ユーザーごとの未読件数を計算して user.unread_count に入れる。
    """
    # 自分がフォローしているユーザーのID一覧
    following_ids = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)

    # 実際に表示するユーザーオブジェクト
    users = User.objects.filter(id__in=following_ids).order_by('username')

    # 未読件数をバルクで取得（sender ごと）
    unread_qs = (
        Message.objects
               .filter(receiver=request.user, sender_id__in=following_ids, is_read=False)
               .values('sender_id')
               .annotate(unread=Count('id'))
    )
    unread_map = {item['sender_id']: item['unread'] for item in unread_qs}

    # users に属性を付ける（テンプレートで使いやすくするため）
    for u in users:
        u.unread_count = unread_map.get(u.id, 0)

    return render(request, 'messengers/inbox.html', {'users': users})

#conversationビューがメッセージの表示と送信の両方を担当
@login_required
def conversation(request, user_id):
    """特定ユーザーとの会話"""
    other_user = get_object_or_404(User, id=user_id)

    # --- POST処理: 送信 ---
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            if check_for_profanity(content):
                messages.error(request, '不適切な言葉が含まれています。メッセージを修正してください。')
            else:
                Message.objects.create(
                    sender=request.user,
                    receiver=other_user,
                    content=content
                )
        return redirect("messengers:conversation", user_id=other_user.id)

    # --- GET処理: 会話表示 ---
    chat_messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user)
    ).order_by('created_at').select_related("sender", "receiver")

    # 未読を既読に更新
    chat_messages.filter(receiver=request.user, is_read=False).update(is_read=True)

    return render(request, "messengers/conversation.html", {
        "chat_messages": chat_messages,
        "other_user": other_user
    })

