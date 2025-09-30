# search/views.py
from django.shortcuts import render
from django.db.models import Q
from blog.models import Post
from tags.models import Tag, UserTag
from users.models import User
from exercise_logs.models import ExerciseLog

def search_view(request):
    query = request.GET.get("q", "").strip()
    print(">>> search_view called")
    print("DEBUG query=", repr(query))

    results = {
        "tags": [],
        "blog_posts": [],
        "users": [],
        "exercise_logs": [],
    }

    if query:
        # --------------------------
        # タグ検索（補助的に表示するだけ）
        # --------------------------
        tags = Tag.objects.filter(name__icontains=query)
        results["tags"] = tags
        print("DEBUG tags=", tags)

        # --------------------------
        # ブログ記事検索（タイトル OR content OR body）
        # --------------------------
        blog_qs = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(body__icontains=query)
        )

        # タグに紐づく記事も追加
        if tags.exists():
            blog_qs = blog_qs | Post.objects.filter(tags__in=tags)

        results["blog_posts"] = blog_qs.distinct().select_related("author").prefetch_related("tags")
        print("DEBUG blog_posts=", results["blog_posts"])

        # --------------------------
        # ユーザー検索（username OR bio）
        # --------------------------
        user_qs = User.objects.filter(
            Q(username__icontains=query) |
            Q(bio__icontains=query)
        )

        # タグに紐づくユーザーも追加
        if tags.exists():
            user_qs = user_qs | User.objects.filter(tags__tag__in=tags)

        results["users"] = user_qs.distinct()
        print("DEBUG users=", results["users"])

        # --------------------------
        # 運動ログ検索（運動名）
        # --------------------------
        exercise_qs = ExerciseLog.objects.filter(
            exercise__name__icontains=query
        )

        # タグに紐づく運動ログも追加
        if tags.exists():
            exercise_qs = exercise_qs | ExerciseLog.objects.filter(tags__in=tags)

        results["exercise_logs"] = exercise_qs.distinct()
        print("DEBUG exercise_logs=", results["exercise_logs"])

    return render(
        request,
        "core/search_results.html",  # ここは既存のテンプレートパスに合わせる
        {"query": query, "results": results}
    )
