from django.db import migrations
from django.utils.text import slugify

def generate_slugs(apps, schema_editor):
    Post = apps.get_model('blog', 'Post')
    for post in Post.objects.all():
        if not post.slug or post.slug.strip() == "":
            # 日本語も対応
            base_slug = slugify(post.title, allow_unicode=True) if post.title else f'post-{post.pk}'
            slug_candidate = base_slug
            counter = 1
            # 同じ slug が存在する場合は末尾に番号を付ける
            while Post.objects.filter(slug=slug_candidate).exclude(pk=post.pk).exists():
                slug_candidate = f"{base_slug}-{counter}"
                counter += 1
            post.slug = slug_candidate
            post.save(update_fields=['slug'])

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20250927_1134'),  # 直前のマイグレーション名に置き換え
    ]

    operations = [
        migrations.RunPython(generate_slugs),
    ]
