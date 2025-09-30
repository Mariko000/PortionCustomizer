# profanity_filter/utils.py
#データベースからNGワードを取得してチェックする関数
from .models import NgWord

def check_for_profanity(text):
    # データベースからすべてのNGワードを取得
    ng_words = NgWord.objects.all()

    # 取得したNGワードでテキストをチェック
    for ng_word in ng_words:
        if ng_word.word in text:
            return True
    return False