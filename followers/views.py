from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model
from .models import Follow, Block

User = get_user_model()
# followers/views.py

class FollowAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(User, id=user_id)
        if request.user == target_user:
            return Response({'message': '自分自身は対象にできません。'}, status=status.HTTP_400_BAD_REQUEST)

        if Follow.objects.filter(follower=request.user, following=target_user).exists():
            # フォロー済みの場合もフォロワー数を返す
            followers_count = Follow.objects.filter(following=target_user).count()
            return Response({'message': 'すでにフォローしています。', 'followers_count': followers_count}, status=status.HTTP_200_OK)

        Follow.objects.create(follower=request.user, following=target_user)
        # 成功した場合、フォロワー数を取得して返す
        followers_count = Follow.objects.filter(following=target_user).count()
        return Response({'message': 'フォローしました。', 'followers_count': followers_count}, status=status.HTTP_201_CREATED)


class UnfollowAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(User, id=user_id)
        deleted_count, _ = Follow.objects.filter(
            follower=request.user,
            following=target_user
        ).delete()

        if deleted_count > 0:
            # フォロー解除後、フォロワー数を取得して返す
            followers_count = Follow.objects.filter(following=target_user).count()
            return Response({'message': 'フォローを解除しました。', 'followers_count': followers_count}, status=status.HTTP_200_OK)
            
        # フォローしていなかった場合もフォロワー数を返す
        followers_count = Follow.objects.filter(following=target_user).count()
        return Response({'message': 'フォローしていません。', 'followers_count': followers_count}, status=status.HTTP_404_NOT_FOUND)
    
class BlockAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(User, id=user_id)
        if request.user == target_user:
            return Response({'message': '自分自身はブロックできません。'}, status=status.HTTP_400_BAD_REQUEST)

        if Block.objects.filter(blocker=request.user, blocked=target_user).exists():
            return Response({'message': 'すでにブロックしています。'}, status=status.HTTP_200_OK)

        # フォロー関係があれば削除してからブロック
        Follow.objects.filter(follower=request.user, following=target_user).delete()
        Follow.objects.filter(follower=target_user, following=request.user).delete()

        Block.objects.create(blocker=request.user, blocked=target_user)
        return Response({'message': 'ブロックしました。'}, status=status.HTTP_201_CREATED)


class UnblockAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(User, id=user_id)
        deleted_count, _ = Block.objects.filter(
            blocker=request.user,
            blocked=target_user
        ).delete()

        if deleted_count > 0:
            return Response({'message': 'ブロックを解除しました。'}, status=status.HTTP_200_OK)
        return Response({'message': 'ブロックしていません。'}, status=status.HTTP_404_NOT_FOUND)
