#__init__.py に Celery を読み込む
#Django をインポートした時点で Celery がロードされる
from .celery import app as celery_app

__all__ = ("celery_app",)
