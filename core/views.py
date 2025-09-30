from django.shortcuts import render
from django.db.models import Q
from blog.models import Post  # blogアプリのPostモデルをインポート
from users.models import User # Userモデルをインポート
from blog.models import Tag  # Tagモデルをインポート


# Create your views here.

def search(request):
    """
    サイト全体のコンテンツを検索するビュー
    """
    query = request.GET.get('q')
    results = {}
    if query:
        # Blogアプリの投稿を検索
        blog_posts = Post.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )
        results['blog_posts'] = blog_posts
        
        # ユーザーを検索
        users = User.objects.filter( # ここでUserモデルを使用
            Q(username__icontains=query) | Q(bio__icontains=query)
        )
        results['users'] = users

        # タグを検索
        tags = Tag.objects.filter(name__icontains=query)
        results['tags'] = tags

        # タグを持つユーザーを検索 (UserTagモデルを経由)
        users_with_tag = User.objects.filter(
            tags__tag__name__icontains=query
        ).distinct()
        results['users_with_tag'] = users_with_tag

    return render(request, 'core/search_results.html', {'results': results, 'query': query})


def home(request):
    """
    ホームページを表示するビュー
    """
    return render(request, 'home.html', {})
