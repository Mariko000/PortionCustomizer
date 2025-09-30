from profanity_filter.utils import check_for_profanity
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
from likes.models import Like
from django.contrib.contenttypes.models import ContentType
from comments.forms import CommentForm
from tags.models import Tag
from exercise_logs.models import ExerciseLog
from django.db.models import Count
from django.http import JsonResponse


# ========================================
# 投稿一覧
# ========================================
def post_list(request):
    sort = request.GET.get('sort', 'newest')
    if sort == 'oldest':
        posts = Post.objects.all().order_by('created_at')
    elif sort == 'comments':
        posts = Post.objects.annotate(num_comments=Count('comments')).order_by('-num_comments', '-created_at')
    elif sort == 'likes':
        posts = Post.objects.annotate(num_likes=Count('likes')).order_by('-num_likes', '-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')

    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'current_sort': sort,
    })

# ========================================
# 投稿詳細
# ========================================
def post_detail(request, pk, slug=None):
    post = get_object_or_404(Post, pk=pk)
    if slug and post.slug and slug != post.slug:
        return redirect(post.get_absolute_url())

    is_liked = False
    exercise_logs = []
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(
            user=request.user,
            object_id=post.pk,
            content_type=ContentType.objects.get_for_model(Post)
        ).exists()
        exercise_logs = ExerciseLog.objects.filter(user=request.user).order_by('-date', '-time')

    form = CommentForm()
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'form': form,
        'is_liked': is_liked,
        'exercise_logs': exercise_logs
    })

# ========================================
# 新規投稿（ガチャ経由の最新運動ログ1件付き）
# ========================================
@login_required
def post_new(request):
    """
    新規投稿画面。
    exercise_logs = [] をデフォルトにし、
    セッションに gacha_completed がある場合のみ最新の from_gacha=True ログ1件を渡す。
    """
    exercise_logs = []

    # 1回だけ取り出す（pop で消す）
    from_gacha = request.session.pop('gacha_completed', False)

    if from_gacha:
        latest_gacha_log = (
            ExerciseLog.objects
            .filter(user=request.user, from_gacha=True)
            .order_by('-performed_at')   # あなたのモデルに合わせて performed_at
            .first()
        )
        if latest_gacha_log:
            exercise_logs = [latest_gacha_log]

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.cleaned_data['content']
            if check_for_profanity(content):
                form.add_error('content', '不適切な言葉が含まれています。')
            else:
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                # タグ処理は既存のまま（あなたの要求通り変更しない）
                tags_str = form.cleaned_data.get("tags", "")
                tag_names = [t.strip() for t in tags_str.split(",") if t.strip()]
                post.tags.clear()
                for name in tag_names:
                    tag, _ = Tag.objects.get_or_create(name=name)
                    post.tags.add(tag)
                return redirect('blog:post_detail', pk=post.pk, slug=post.slug)
    else:
        form = PostForm()

    return render(request, 'blog/post_form.html', {
        'form': form,
        'page_title': '新しい投稿',
        'exercise_logs': exercise_logs,
    })

# ========================================
# 投稿編集
# ========================================
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return redirect('blog:post_detail', pk=post.pk, slug=post.slug)

    exercise_logs = ExerciseLog.objects.filter(user=request.user).order_by('-date', '-time')

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            content = form.cleaned_data['content']
            if check_for_profanity(content):
                form.add_error('content', '不適切な言葉が含まれています。投稿内容を修正してください。')
            else:
                post = form.save(commit=False)
                post.author = request.user
                post.save()  # save() 内で slug 生成済み

                # タグ処理
                tags_str = form.cleaned_data.get("tags", "")
                tag_names = [t.strip() for t in tags_str.split(",") if t.strip()]
                post.tags.clear()
                for name in tag_names:
                    tag, _ = Tag.objects.get_or_create(name=name)
                    post.tags.add(tag)

                return redirect('blog:post_detail', pk=post.pk, slug=post.slug)
    else:
        tags_str = ", ".join([t.name for t in post.tags.all()])
        form = PostForm(instance=post, initial={'tags': tags_str})

    return render(request, 'blog/post_form.html', {
        'form': form,
        'page_title': '投稿を編集',
        'exercise_logs': exercise_logs,
    })

# ========================================
# 選択削除
# ========================================
@login_required
def delete_selected_posts(request):
    if request.method == "POST":
        # Ajaxリクエスト判定
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

        selected_ids = request.POST.get('selected_posts', '')
        ids_list = [int(pk) for pk in selected_ids.split(',') if pk.isdigit()]

        # 投稿者が request.user の投稿のみ削除
        posts_to_delete = Post.objects.filter(pk__in=ids_list, author=request.user)
        count = posts_to_delete.count()
        posts_to_delete.delete()


        from .models import Post
        posts_to_delete = Post.objects.filter(pk__in=ids_list, author=request.user)
        count = posts_to_delete.count()
        posts_to_delete.delete()


        if is_ajax:
            return JsonResponse({"error": False, "deleted_count": count})
        else:
            # 通常のPOSTならリダイレクト
            from django.shortcuts import redirect
            return redirect('blog:post_list')

    return JsonResponse({"error": True, "message": "Invalid request"})

# ========================================
# 全削除
# ========================================
@login_required
def delete_all_posts(request):
    if request.method == "POST":
        deleted_count = Post.objects.filter(author=request.user).delete()[0]
        return JsonResponse({'error': False, 'deleted_count': deleted_count})

    return JsonResponse({'error': True, 'message': 'Invalid request'}, status=400)

# ========================================
# いいね機能 (Ajax専用)
# ========================================

@login_required
def post_like(request, pk):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        post = get_object_or_404(Post, pk=pk)
        content_type = ContentType.objects.get_for_model(Post)
        like, created = Like.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=post.pk
        )
        if not created:
            like.delete()

        likes_count = post.likes.count()
        is_liked = Like.objects.filter(
            user=request.user,
            content_type=content_type,
            object_id=post.pk
        ).exists()

        return JsonResponse({
            'likes_count': likes_count,
            'is_liked': is_liked
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)


# ========================================
# 運動ログ一覧
# ========================================
@login_required
def exercise_log_list(request):
    logs = ExerciseLog.objects.filter(user=request.user).order_by('-date', '-time')
    return render(request, 'blog/exercise_log_list.html', {'logs': logs})
