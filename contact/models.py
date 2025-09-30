from django.db import models
from django.utils import timezone

class ContactMessage(models.Model):
    """
    ユーザーからのお問い合わせメッセージを保存するモデル
    """
    name = models.CharField('お名前', max_length=100)
    email = models.EmailField('メールアドレス')
    message = models.TextField('メッセージ')
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        """
        管理サイトで表示されるオブジェクトの文字列表現
        """
        return f'{self.name} - {self.email}'

    class Meta:
        verbose_name = 'お問い合わせメッセージ'
        verbose_name_plural = 'お問い合わせメッセージ'
