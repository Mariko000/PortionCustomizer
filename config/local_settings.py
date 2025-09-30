# local_settings.py（開発用）
DEBUG = True
SECRET_KEY = "開発用の秘密鍵"
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}
