# FitSpin

FitSpin はフィットネス管理アプリです。

## 特徴
- ワークアウトの記録
- タイマー機能
- ステータス管理

## インストール

1. リポジトリをクローン
```bash
git clone https://github.com/Mariko000/FitSpin.git
cd FitSpin

仮想環境作成
python -m venv env

仮想環境をアクティベート
source env/bin/activate

必要パッケージをインストール


pip install -r requirements.txt
サードパーティパッケージ
django

django-imagekit (画像の自動リサイズや処理)

django-webpush (プッシュ通知)

djangorestframework (REST API 開発用)

django-cors-headers (CORS 設定)

django-allauth (SNS 認証 / ユーザー管理)

django-crispy-forms (フォームの見た目整形)

crispy-bootstrap5 (Bootstrap5 用テンプレートパック)

celery (非同期タスク)

redis (Celery ブローカー)

profanity-filter (不適切ワードチェック)

Vue.js 側で Font Awesome を使う場合：
npm install --save @fortawesome/fontawesome-free

Vue.js の依存関係をインストール
npm install

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

