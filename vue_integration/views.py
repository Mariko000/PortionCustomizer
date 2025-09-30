# vue_integration/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from users.models import User # カスタムユーザーモデルをインポート
import json
import os


def vue_index(request):
    if settings.DEBUG:
        # 開発モードは Vite の dev-server をそのまま読む
        return render(request, 'vue_index.html', {
            'js_file': 'http://localhost:5173/src/main.js',
            'css_files': [],
            'debug': True,
        })
    else:
        # ビルド済みファイル
        manifest_path = os.path.join(settings.BASE_DIR, 'static/vue/manifest.json')
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        main = manifest['src/main.js']
        return render(request, 'vue_index.html', {
            'js_file': f"/static/vue/{main['file']}",
            'css_files': [f"/static/vue/{c}" for c in main.get('css', [])],
            'debug': False,
        })
    
@login_required
def current_user(request):
    user = request.user  

    # avatar_thumbnail がある場合はURLに変換
    avatar_url = user.avatar_thumbnail.url if user.avatar else None

    return JsonResponse({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "bio": user.bio,
        "avatar": avatar_url,
        "status_level": user.status_level,
    })