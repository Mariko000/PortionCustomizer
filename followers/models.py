from django.db import models
from django.conf import settings

class Follow(models.Model):
    """
    ユーザーのフォロー関係を定義するモデル
    """
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='following_set',
        on_delete=models.CASCADE,
        verbose_name='フォローしているユーザー'
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='follower_set',
        on_delete=models.CASCADE,
        verbose_name='フォローされているユーザー'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
        verbose_name = 'フォロー'
        verbose_name_plural = 'フォロー'

    def __str__(self):
        return f'{self.follower.username} が {self.following.username} をフォロー'

class Block(models.Model):
    blocker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='blocking_set',
        on_delete=models.CASCADE,
        verbose_name='ブロックするユーザー'
    )
    blocked = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='blocked_by_set',
        on_delete=models.CASCADE,
        verbose_name='ブロックされるユーザー'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('blocker', 'blocked')
        verbose_name = 'ブロック'
        verbose_name_plural = 'ブロック'

    def __str__(self):
        return f'{self.blocker.username} が {self.blocked.username} をブロック'