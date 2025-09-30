from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # 詳細画面に email, points, status_level を追加
    fieldsets = BaseUserAdmin.fieldsets + (
        ('プロフィール', {'fields': ('points', 'status_level')}),
    )

    # 一覧画面に email, points, status_level を追加
    list_display = BaseUserAdmin.list_display + ('email', 'points', 'status_level',)

    # （オプション）検索対象にemailを追加
    search_fields = BaseUserAdmin.search_fields + ('email',)
