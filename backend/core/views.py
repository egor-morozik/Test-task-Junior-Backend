from typing import Any, cast

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.pagination import CursorPagination

from django.db.models import QuerySet

from core.models import Post, Comment
from core.serializers import (
    PostSerializer,
    CommentCreateSerializer,
    CommentReadSerializer,
)
from core.services import InstagramService
from core.clients import instagram_client


class PostCursorPagination(CursorPagination):
    page_size: int = 10
    ordering: str = "-timestamp"


class SyncMediaView(generics.CreateAPIView):
    """
    Синхронизировать посты в базе данных и Instagram.
    """

    queryset: QuerySet[Post] = Post.objects.none()

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        count: int = InstagramService(instagram_client).sync_all_posts()
        return Response(
            {
                "synced": count,
            },
            status=status.HTTP_201_CREATED,
        )


class PostListView(generics.ListAPIView):
    """
    Получить из базы данных все посты Instagram.
    """

    queryset: QuerySet[Post] = Post.objects.all()
    serializer_class: type[PostSerializer] = PostSerializer
    pagination_class: type[PostCursorPagination] = PostCursorPagination


class CommentCreateView(generics.CreateAPIView):
    """
    Написать комменатрий для поста из базы данных комменатрий в Instagram.
    """

    serializer_class: type[CommentCreateSerializer] = CommentCreateSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = cast(
            CommentCreateSerializer, self.get_serializer(data=request.data)
        )
        serializer.is_valid(raise_exception=True)

        comment: Comment = InstagramService(instagram_client).add_comment(
            post_pk=self.kwargs["pk"],
            text=serializer.validated_data["text"],
        )
        return Response(
            CommentReadSerializer(comment).data,
            status=status.HTTP_201_CREATED,
        )
