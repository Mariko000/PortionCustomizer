from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db.models import Count
from .models import Tag
#このシリアライザは、Userモデルの情報に加えて、フォロワー数、フォロー数、共通タグといった動的なデータを追加します

User = get_user_model()

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name"]

class UserListSerializer(serializers.ModelSerializer):
    """
    ユーザー一覧表示用のシリアライザ
    フォロワー数、フォロー数、タグ情報を追加
    """
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    
    # 共通タグを計算するためのフィールド
    common_tags = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ["id", "username", "bio", "avatar", "tags", "followers_count", "following_count", "common_tags"]
        
    def get_common_tags(self, obj):
        request_user = self.context.get('request_user')
        if not request_user or not request_user.is_authenticated:
            return []
            
        request_user_tags = set(request_user.tags.values_list('name', flat=True))
        obj_tags = set(obj.tags.values_list('name', flat=True))
        
        common_tag_names = list(request_user_tags.intersection(obj_tags))
        return common_tag_names
