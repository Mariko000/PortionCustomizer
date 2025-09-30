"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# プロジェクトルート上のurls.py
from django.contrib import admin
from . import views
from django.urls import path, include
from core import views as core_views # coreアプリのビューをインポート
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.urls import path, include, re_path

urlpatterns = [
    path('about/', views.about_page, name='about_page'),
    path('explained_design/', views.explained_design, name='explained_design'),
    path('my_skills/', views.my_skills, name='my_skills'),
    path('admin/', admin.site.urls),
    # allauthのURL設定をインクルード
    path('accounts/', include('allauth.urls')),
    # ユーザー関連のHTMLページを管理
    path('users/', include('users.urls')),
    # ユーザー関連のAPIエンドポイントを管理
    path('api/users/', include('users.api.urls')),
    path('', core_views.home, name='home'),
    path('blog/', include('blog.urls')),
    path('comments/', include('comments.urls')),
    path('contact/', include('contact.urls')),
    path('search/', include('search.urls')),
    path("messengers/", include("messengers.urls")), 

    
    # フォロー関連のAPIエンドポイントを管理
    path('api/followers/', include('followers.urls')),

]

# メディアファイルを開発環境で配信する設定
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
