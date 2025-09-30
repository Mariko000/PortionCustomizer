from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from .forms import CommentForm
from .models import Comment
from blog.models import Post

@login_required
def add_comment(request):
    """
    ブログ投稿にコメントを追加するビュー。
    """
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            
            # content_typeとobject_idを取得
            content_type_id = request.POST.get('content_type_id')
            object_id = request.POST.get('object_id')

            try:
                # object_idを使用して、投稿のインスタンスを実際に取得
                post_instance = get_object_or_404(Post, pk=object_id)
                content_type = ContentType.objects.get_for_model(post_instance)
                
                comment.content_type = content_type
                comment.object_id = object_id
                
                comment.save()  # コメントをデータベースに保存
                
                # コメントが保存されたら、元の投稿詳細ページにリダイレクト
                return redirect(post_instance.get_absolute_url())

            except (ValueError, ContentType.DoesNotExist):
                # エラーが発生した場合でも元の投稿ページにリダイレクト
                return redirect('blog:post_detail', pk=object_id)
    
    # POSTメソッド以外、またはフォームが無効な場合は、元の投稿ページにリダイレクト
    object_id = request.POST.get('object_id')
    return redirect('blog:post_detail', pk=object_id)
