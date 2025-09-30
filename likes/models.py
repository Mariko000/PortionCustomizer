from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

class Like(models.Model):
    """
    ユーザーが特定のオブジェクトに「いいね」をしたことを記録するモデル。
    GenericForeignKeyを使用して、様々なモデル（例：Post, Comment）に対応可能。
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    
    # いいねの対象となるオブジェクト
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 一人のユーザーが一つのオブジェクトに複数回いいねできないようにする
        unique_together = ('user', 'content_type', 'object_id')
        verbose_name = 'いいね'
        verbose_name_plural = 'いいね'

    def __str__(self):
        return f"{self.user.username}がいいねした {self.content_object}"

