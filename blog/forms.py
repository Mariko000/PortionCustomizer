from django import forms
from .models import Post
from tags.models import Tag

class PostForm(forms.ModelForm):
    """
    ブログ記事の投稿・編集用フォーム
    """
    #タグ
    tags = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
        label='タグ',
        help_text="タグをカンマ区切りで入力（例: Python, Django, Vue）",
    )


    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'tags' ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }

