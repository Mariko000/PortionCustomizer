from django import forms
from .models import User
from allauth.account.forms import SignupForm, LoginForm
from django.core.exceptions import ValidationError
from tags.models import Tag, UserTag

class UserUpdateForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="カンマ区切りでタグを入力してください （例: プログラミング, インテリア, アニメ）"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'avatar', 'bio']

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()

        # --- タグ処理 ---
        tags_str = self.cleaned_data.get('tags', '')
        tag_names = [name.strip() for name in tags_str.split(',') if name.strip()]

        UserTag.objects.filter(user=user).delete()
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            UserTag.objects.get_or_create(user=user, tag=tag)

        return user

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["login"].widget.attrs.update({
            "placeholder": "ユーザー名 または メールアドレス",
            "class": "form-control",
        })
        self.fields["password"].widget.attrs.update({
            "placeholder": "パスワード",
            "class": "form-control",
        })


class CustomSignupForm(SignupForm):
    """
    allauthのデフォルトSignupFormを継承したカスタムフォームです。
    ユーザー登録時に入力項目をカスタマイズする場合に使用します。
    """
    avatar = forms.ImageField(required=False, label='アバター画像', widget=forms.FileInput)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("このメールアドレスは既に使用されています。")
        return email

    def save(self, request):
        user = super().save(request)
        user.avatar = self.cleaned_data.get('avatar')
        user.save()
        return user
