from django.urls import reverse
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Tag(models.Model):
    """
    ユーザーの興味を管理するためのタグモデル
    例: Python, Django, Vue.js
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    ユーザー認証とプロフィールを拡張するカスタムユーザーモデル
    """

    email = models.EmailField(unique=True)

    avatar = models.ImageField(
        verbose_name='プロフィール画像',
        upload_to='profile_pictures/',
        null=True,
        blank=True,
    )
    
    avatar_thumbnail = ImageSpecField(
        source='avatar',
        processors=[ResizeToFill(50, 50)],
        format='JPEG',
        options={'quality': 80}
    )

    bio = models.TextField(max_length=500, blank=True)

    last_login_time = models.DateTimeField(null=True, blank=True)
    login_streak = models.IntegerField(default=0)

    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True
    )

    # 運動レベルとポイント
    status_level = models.PositiveIntegerField(default=1, verbose_name='運動レベル', help_text='1〜5の運動レベル')
    points = models.IntegerField(default=0)

    def add_points(self, amount: int):
        """
        ポイントを加算し、必要に応じて1レベルずつ上げる
        """
        self.points += amount
        # 1レベルずつ上がる
        if self.points >= self._points_needed_for_next_level() and self.status_level < 5:
            self.status_level += 1
        self.save(update_fields=['points', 'status_level'])

    def _points_needed_for_next_level(self) -> int:
        """
        次のレベルに必要なポイント
        """
        points_table = {1: 50, 2: 100, 3: 200, 4: 400}  # レベル5は最大
        return points_table.get(self.status_level, 9999)

    class Meta:
        db_table = 'users'
        verbose_name = 'ユーザー'
        verbose_name_plural = 'ユーザー'
        
    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse('users:user_profile_detail', args=[self.pk])


class LoginHistory(models.Model):
    """
    ユーザーのログイン履歴を記録するモデル
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    login_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'ログイン履歴'
        verbose_name_plural = 'ログイン履歴'
        ordering = ['-login_date']
        unique_together = ('user', 'login_date')

    def __str__(self):
        return f"{self.user.username} logged in on {self.login_date}"
