from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import ContactForm
from .models import ContactMessage
from profanity_filter.utils import check_for_profanity
from django.shortcuts import render, redirect

def contact(request):
    """
    コンタクトフォームを表示・処理するビュー
    セッションベースで動作しています: 
    メッセージはサーバーのセッションストアに一時的に保存され、
    ブラウザのクッキーを通じてユーザーに紐づけられます。メッセージは表示された後に削除されるため、
    サーバーのデータベースに永続的に残ることはありません
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # NGワードのチェックを追加
            message_content = form.cleaned_data['message']
            if check_for_profanity(message_content):
                messages.error(request, '不適切な言葉が含まれています。メッセージを修正してください。')
                return render(request, 'contact/contact.html', {'form': form})
            else:
                # フォームのデータを取得してデータベースに保存
                ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            messages.success(request, 'お問い合わせありがとうございます。')
            return redirect(reverse_lazy('contact:contact_success'))
    else:
        form = ContactForm()
    
    return render(request, 'contact/contact.html', {'form': form})



def contact_success(request):
    return render(request, 'contact/success.html')

