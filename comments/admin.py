from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'created_at', 'content_object')
    list_filter = ('created_at',)
    search_fields = ('text', 'author__username')