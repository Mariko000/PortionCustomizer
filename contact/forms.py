from django import forms

class ContactForm(forms.Form):
    """
    コンタクトフォーム
    """
    name = forms.CharField(max_length=100, label='お名前', help_text='お名前を入力してください')
    email = forms.EmailField(label='メールアドレス', help_text='返信先のメールアドレスを入力してください')
    message = forms.CharField(label='メッセージ', widget=forms.Textarea, help_text='メッセージを入力してください')

