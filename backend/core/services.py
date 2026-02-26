from typing import Any, Dict, Generator, List, Optional, Union, cast

from django.utils.timezone import now
from django.db import transaction

from rest_framework.exceptions import ValidationError, NotFound

from core.models import Post, Comment
from core.serializers import PostSerializer, CommentReadSerializer
from core.clients import InstagramClient


class InstagramService:
    """
    Бизнес-логика синхронизации и взаимодействия с Instagram API.
    """

    MEDIA_FIELDS: List[str] = [
        "id",
        "caption",
        "media_url",
        "permalink",
        "timestamp",
    ]

    COMMENT_FIELDS: List[str] = [
        "id",
        "text",
        "username",
        "timestamp",
    ]

    def __init__(self, client: InstagramClient) -> None:
        self._client: InstagramClient = client
        self._media_fields_str: str = ",".join(self.MEDIA_FIELDS)
        self._comment_fields_str: str = ",".join(self.COMMENT_FIELDS)

    def _fetch_pages(
        self, path: Optional[str], params: Dict[str, Any]
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Генератор для обхода всех страниц пагинации API Instagram.
        """

        while path:
            resource: Dict[str, Any] = self._client.get(path, params=params)
            yield from resource.get("data", [])

            next_url: Optional[str] = resource.get("paging", {}).get("next")
            path = (
                next_url.replace(self._client.BASE_URL, "").lstrip("/")
                if next_url
                else None
            )
            params = {}

    def _sync_comments(self, post: Post) -> None:
        """
        Синхронизация комментариев под постом в Instagram.
        """

        path: str = f"{post.ig_id}/comments"
        params: Dict[str, Any] = {
            "fields": self._comment_fields_str,
        }
        for item in self._fetch_pages(path, params):
            serializer = CommentReadSerializer(data=item)
            if serializer.is_valid():
                serializer.save(post=post)

    def sync_all_posts(self) -> int:
        """
        Синхронизирует все посты в базу данных из Instagram.
        """

        params: Dict[str, Any] = {
            "fields": self._media_fields_str,
            "limit": 50,
        }
        count: int = 0

        with transaction.atomic():
            for item in self._fetch_pages("me/media", params):
                serializer = PostSerializer(data=item)
                if serializer.is_valid():
                    post = cast(Post, serializer.save())
                    self._sync_comments(post)
                    count += 1
        return count

    def add_comment(self, post_pk: Union[int, str], text: str) -> Comment:
        """
        Отправляет к посту из базы данных комментарий в Instagram.
        """

        try:
            post: Post = Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            raise NotFound(f"Пост с id {post_pk} не найден в базе данных.")

        try:
            resource: Dict[str, Any] = self._client.post(
                f"{post.ig_id}/comments",
                data={
                    "message": text,
                },
            )
        except Exception as e:
            raise ValidationError(f"Ошибка Instagram: {str(e)}")

        return Comment.objects.create(
            post=post,
            ig_id=resource["id"],
            text=text,
            username="me",
            timestamp=now(),
        )
