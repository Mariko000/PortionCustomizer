# FitSpin

PortionCustomizerはレシピ調整補助のためのアプリです。


## 特徴
- 開発中

## インストール

# ==============================================
# Mac / Linux 用 必須コマンド集
# （Python + Node + Redis + Django 開発環境）
# ==============================================

# 1. 仮想環境作成 & 有効化
python3 -m venv env
source env/bin/activate

# 2. pip を最新にアップグレード
pip install --upgrade pip

# 3. Python パッケージ一括インストール
pip install django==5.1.1 \
djangorestframework \
django-cors-headers \
django-allauth \
django-crispy-forms \
crispy-bootstrap5 \
django-imagekit \
django-webpush \
django-profanity-filter \
pillow \
celery \
redis \
python-dotenv \
black \
isort \
flake8

# 4. Node.js インストール（Homebrew）
brew install node

# 5. Vue プロジェクト依存インストール
cd vue-contents
npm install
npm run dev   # 開発用サーバー起動

# 6. Redis 起動（Celery 用）
brew install redis
brew services start redis

# 7. Django 初期設定
python manage.py migrate
python manage.py createsuperuser  # 必要に応じて
python manage.py runserver

使い方
Django 開発サーバー

python manage.py runserver

ブラウザでアクセス：
http://127.0.0.1:8000/

Vue.js 開発サーバー

npm run dev

ブラウザでアクセス：
http://localhost:5173/

ポイント: Django と Vue.js は 両方同時に起動する必要があります。

本番環境

npm run build

仮想環境の無効化
deactivate

データベースマイグレーション

python manage.py makemigrations
python manage.py migrate

開発時は Django と Vue.js 両方のサーバーを走らせて確認

本番環境では Vue.js をビルドして Django に統合

