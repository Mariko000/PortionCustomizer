# tags/models.py
#「プリセット（固定リスト）」＋「ユーザー追加タグ」ハイブリッド方式
from django.urls import reverse
from django.db import models
from django.conf import settings

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_preset = models.BooleanField(default=False)  # Trueなら固定リスト
    def __str__(self):
        return self.name
    


class UserTag(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tags")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="users")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tag')
