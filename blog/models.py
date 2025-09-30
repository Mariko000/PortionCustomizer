from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from tags.models import Tag
from django.utils.text import slugify

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='タイトル')
    content = models.TextField(verbose_name='本文')
    body = models.TextField()
    image = models.ImageField(
        verbose_name='画像',
        upload_to='blog_images/',
        null=True,
        blank=True,
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='著者')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新日時')
    is_published = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0, verbose_name='閲覧数')

    slug = models.SlugField(max_length=255, blank=True, unique=True)

    comments = GenericRelation('comments.Comment')
    likes = GenericRelation('likes.Like')
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk, 'slug': self.slug})

    class Meta:
        verbose_name = '投稿'
        verbose_name_plural = '投稿'
        ordering = ['-created_at']

    # ==========================
    # save() で slug を強制生成（日本語対応）
    # ==========================
    def save(self, *args, **kwargs):
        # 新規作成で pk がまだない場合は一度保存して pk を確定
        if not self.pk:
            super().save(*args, **kwargs)

        if not self.slug or self.slug.strip() == "":
            # allow_unicode=True で日本語タイトルも slug に変換可能
            base_slug = slugify(self.title, allow_unicode=True) if self.title else f'post-{self.pk}'
            slug_candidate = base_slug
            counter = 1
            # 同じ slug が存在する場合は末尾に番号を付与
            while Post.objects.filter(slug=slug_candidate).exclude(pk=self.pk).exists():
                slug_candidate = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug_candidate

        super().save(*args, **kwargs)
