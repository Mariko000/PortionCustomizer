#users/views.py
import json
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Prefetch
from .forms import UserUpdateForm
from .models import LoginHistory
from tags.models import UserTag
import datetime
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.db.models import Count
from .serializers import UserListSerializer
from followers.models import Follow
from blog.models import Post
import random
from followers.models import Follow, Block
from datetime import date, timedelta

#
User = get_user_model()

@login_required
def profile_update(request):
    """
    ユーザープロフィールとアバター画像を更新します。
    """
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:user_profile')
    else:
        form = UserUpdateForm(instance=request.user)
        # 初期値に既存タグを入れる
        initial_tags = ", ".join([ut.tag.name for ut in request.user.tags.all()])
        form = UserUpdateForm(instance=request.user, initial={"tags": initial_tags})
    
    return render(request, 'account/profile_update.html', {'form': form})

#継続ログイン日数 & レベル計算
def update_login_streak(user):
    """
    連続ログイン日数を更新し、運動レベルも計算する
    """
    today = date.today()

    # Userモデルには last_login_time があるのでそれを参照
    last_login_date = user.last_login_time.date() if user.last_login_time else None

    # 今日ログイン済みなら何もしない
    if last_login_date == today:
        return

    # 連続ログイン日数の更新
    if last_login_date == today - timedelta(days=1):
        user.login_streak += 1
    else:
        user.login_streak = 1

    # last_login_time を今日に更新
    user.last_login_time = datetime.datetime.now()
    user.save(update_fields=['login_streak', 'last_login_time'])

    # LoginHistory にも記録
    LoginHistory.objects.get_or_create(user=user, login_date=today)

    # streak に応じた運動レベル計算（例: 3日ごとに1レベルUP、最大5）
    streak = user.login_streak
    calculated_level = min(1 + streak // 3, 5)
    if user.status_level < calculated_level:
        user.status_level = calculated_level
        user.save(update_fields=['status_level'])


@login_required
def login_calendar(request):
    """
    ユーザーのログイン履歴カレンダーを表示します。
    """
    login_dates = LoginHistory.objects.filter(user=request.user).values_list('login_date', flat=True)
    login_dates_str = [d.strftime('%Y-%m-%d') for d in login_dates]
    
    context = {
        'user': request.user,
        'login_dates': login_dates_str,
    }
    return render(request, 'account/login_calendar.html', context)

#Vueで同じログイン履歴を使うのでAPIとしてJSONで返すビューを追加
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def login_history_api(request):
    """ログイン履歴をJSONで返す"""
    login_dates = LoginHistory.objects.filter(user=request.user).values_list('login_date', flat=True)
    dates_str = [d.strftime('%Y-%m-%d') for d in login_dates]
    return JsonResponse({"login_dates": dates_str})


@login_required
def user_profile(request):
    """
    ログイン中のユーザープロフィールを表示します。
    """
     # ログイン中のユーザーを取得
    profile_user = request.user

    # フォロワー一覧（自分をフォローしている人）
    followers = [f.follower for f in Follow.objects.filter(following=profile_user).select_related("follower")]
    # フォロー中一覧（自分がフォローしている人）
    following = [f.following for f in Follow.objects.filter(follower=profile_user).select_related("following")]

    
    # フォロワー数とフォロー数を取得
    followers_count = Follow.objects.filter(following=profile_user).count()
    following_count = Follow.objects.filter(follower=profile_user).count()

    # タグ一覧を取得（UserTag経由でTagを取る）
    tags = [ut.tag.name for ut in profile_user.tags.all()]
    
    context = {
        'profile_user': profile_user,
        'followers_count': followers_count,
        'following_count': following_count,
        'followers': followers,
        'following': following,
        'tags': tags,
    }
    return render(request, 'account/user_profile.html', context)

def user_profile_detail(request, user_id):
    """
    他人のプロフィール
    """
    profile_user = get_object_or_404(User, id=user_id)

    followers = Follow.objects.filter(following=profile_user).select_related("follower")
    following = Follow.objects.filter(follower=profile_user).select_related("following")

    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=profile_user
        ).exists()

    posts = Post.objects.filter(author=profile_user).order_by("-created_at")
    user_tags = profile_user.tags.select_related("tag").all()

    context = {
        "profile_user": profile_user,
        "followers": [f.follower for f in followers],
        "following": [f.following for f in following],
        "followers_count": followers.count(),
        "following_count": following.count(),
        "is_following": is_following,
        "posts": posts,
        "user_tags": user_tags,
    }
    return render(request, "account/other_user_detail.html", context)

#GETリクエストのみを受け付けるAPIビューであることを示す
#ログイン済みのユーザーだけがこのAPIにアクセスできる
#認証されていない場合は、自動的に403 Forbiddenエラーが返されます
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_info(request):
    """
    ログイン中のユーザー情報を返すAPIエンドポイント
    """
    # ユーザーが認証されている場合、その情報をJSONで返す
    return JsonResponse({
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email,
        'status_level': request.user.status_level,
        'points': request.user.points
    })


# API用のUserListViewをここに追加
class UserListView(generics.ListAPIView):
    """
    全てのユーザーをリストするAPIビュー。
    フォロワー数でソートされます。
    """
    queryset = get_user_model().objects.all().annotate(followers_count=Count('followers')).order_by('-followers_count')
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]

@login_required
def user_list_page(request):
    """
    ユーザー一覧ページ
    - 全ユーザー一覧（自分＆ブロック済みを除外）
    - おすすめユーザー一覧（共通フォロー・共通タグ・ランダム）
    """
    current_user = request.user

    # -------------------------------
    # 0. ブロック済みユーザー＆フォロー中ID
    # -------------------------------
    blocked_ids = set(Block.objects.filter(blocker=current_user).values_list("blocked__id", flat=True))
    following_ids = set(Follow.objects.filter(follower=current_user).values_list('following__id', flat=True))

    # -------------------------------
    # 1. 全ユーザー（自分とブロック済みを除外）
    # -------------------------------
    users = (
        User.objects.exclude(id=current_user.id)
            .exclude(id__in=blocked_ids)
            .annotate(
                followers_count=Count('follower_set', distinct=True),
                following_count=Count('following_set', distinct=True),
            )
            .order_by('-followers_count')
            .prefetch_related(
                Prefetch(
                    'tags',
                    queryset=UserTag.objects.select_related('tag'),
                    to_attr='prefetched_user_tags'
                )
            )
    )
    for u in users:
        u.is_following = u.id in following_ids
        u.is_blocked = u.id in blocked_ids

    # -------------------------------
    # 2. おすすめユーザー（ブロック済みを除外）
    # -------------------------------
    # 共通フォロー
    common_followers_ids = User.objects.filter(
        follower_set__following__in=following_ids
    ).exclude(
        Q(id=current_user.id) | Q(id__in=following_ids) | Q(id__in=blocked_ids)
    ).distinct().values_list('id', flat=True)

    # 共通タグ
    user_tags_ids = UserTag.objects.filter(user=current_user).values_list('tag__id', flat=True)
    common_tags_ids = User.objects.filter(
        tags__tag__in=user_tags_ids
    ).exclude(
        Q(id=current_user.id) | Q(id__in=following_ids) | Q(id__in=blocked_ids)
    ).distinct().values_list('id', flat=True)

    # ランダムユーザー
    exclude_ids = set(following_ids) | {current_user.id} | set(blocked_ids)
    all_others_ids = list(User.objects.exclude(id__in=exclude_ids).values_list('id', flat=True))
    random_users_ids = random.sample(all_others_ids, min(5, len(all_others_ids))) if all_others_ids else []

    # 重複排除
    recommended_user_ids = set(common_followers_ids) | set(common_tags_ids) | set(random_users_ids)

    # おすすめユーザー取得
    recommended_users = (
        User.objects.filter(id__in=recommended_user_ids)
        .annotate(
            followers_count=Count('follower_set', distinct=True),
            following_count=Count('following_set', distinct=True),
        )
        .prefetch_related(
            Prefetch(
                'tags',
                queryset=UserTag.objects.select_related('tag'),
                to_attr='prefetched_user_tags'
            )
        )
    )
    for u in recommended_users:
        u.is_following = u.id in following_ids
        u.is_blocked = u.id in blocked_ids

    context = {
        'users': users,  
        'recommended_users': recommended_users[:10],  # 最大10人
    }
    return render(request, 'account/userlist.html', context)


@login_required
def unlock_next_view(request):
    # ただテンプレートを返す
    #unlock_next.html を返すだけ（ポイント消費しない）
    return render(request, 'account/unlock_next.html', {'user': request.user})


 # ポイント消費でレベルアップできるようにする 
def level_up_by_points(user, points_to_use=15):
    current_level = getattr(user, 'status_level', 1)
    points = getattr(user, 'points', 0)

    if current_level >= 5:
        return False

    if points >= points_to_use:
        user.points -= points_to_use
        user.status_level = current_level + 1
        user.save(update_fields=['points', 'status_level'])
        return True
    else:
        return False

    
@csrf_exempt  # CSRF トークンを利用する場合は不要
@require_POST
@login_required
def level_up_api(request):
    """
    POST: { "points_to_use": 15 } でポイントを消費してレベルアップ
    """
    user = request.user
    try:
        data = json.loads(request.body)
        points_to_use = int(data.get("points_to_use", 15))
    except (json.JSONDecodeError, ValueError, TypeError):
        points_to_use = 15

    level_up_success = level_up_by_points(user, points_to_use=points_to_use)

    response_data = {
        "level_up": level_up_success,
        "current_level": user.status_level,
        "remaining_points": user.points,
    }
    return JsonResponse(response_data)


    
# 共通：レベルアップ判定用関数
def check_level_up(user):
    """
    ポイントと連続ログイン日数を条件にレベルアップ
    条件例:
      - レベル1→2: ポイント10以上かつ連続ログイン3日以上
      - レベル2→3: ポイント20以上かつ連続ログイン5日以上
      - レベル3→4: ポイント30以上かつ連続ログイン7日以上
      - レベル4→5: ポイント50以上かつ連続ログイン10日以上
    """
    level = getattr(user, 'status_level', 1)
    streak = getattr(user, 'login_streak', 0)  # update_login_streakで更新される想定
    points = getattr(user, 'points', 0)

    new_level = level  # 初期値は現レベル

    if level == 1 and points >= 10 and streak >= 3:
        new_level = 2
    elif level == 2 and points >= 20 and streak >= 5:
        new_level = 3
    elif level == 3 and points >= 30 and streak >= 7:
        new_level = 4
    elif level == 4 and points >= 50 and streak >= 10:
        new_level = 5

    # 「今より高い場合だけ」更新
    if new_level > level:
        user.status_level = new_level
        user.save(update_fields=['status_level'])
