import pytest

from typing import Any, Dict

from unittest.mock import MagicMock, patch

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.response import Response

from requests.exceptions import HTTPError

from core.models import Post, Comment


@pytest.mark.django_db
class TestCommentCreateView:
    """
    Интеграционные тесты для эндпоинта создания комментария к посту базы данных.
    POST /api/posts/{id}/comment/
    """

    def get_url(self, post_id: int) -> str:
        return reverse(
            "comment-create",
            kwargs={
                "pk": post_id,
            },
        )

    @patch("core.clients.instagram_client.post")
    def test_create_comment_success(
        self, mock_post: MagicMock, api_client: APIClient, sample_post: Post
    ) -> None:
        """
        1. Успешный запрос: запись в БД создана, ответ API корректен.
        """

        mock_post.return_value = {
            "id": "ig_comment_999",
        }

        payload: Dict[str, str] = {
            "text": "тестовый комментарий",
        }
        url: str = self.get_url(sample_post.id)  # type: ignore

        response: Response = api_client.post(
            url,
            payload,
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] == "ig_comment_999"
        assert response.data["text"] == payload["text"]

        assert Comment.objects.filter(
            ig_id="ig_comment_999",
            post=sample_post,
        ).exists()
        mock_post.assert_called_once()

    def test_create_comment_post_not_found_in_db(
        self, api_client: APIClient, db: Any
    ) -> None:
        """
        2. Ошибка: пост с таким {id} не существует в локальной базе.
        """

        url: str = self.get_url(9999)
        response: Response = api_client.post(
            url,
            {
                "text": "hello world",
            },
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert Comment.objects.count() == 0

    @patch("core.clients.instagram_client.post")
    def test_create_comment_not_in_instagram(
        self, mock_post: MagicMock, api_client: APIClient, sample_post: Post
    ) -> None:
        """
        3. Ошибка: пост есть в базе данных, но удален в Instagram.
        """

        mock_post.side_effect = HTTPError("Media not found or deleted")

        url: str = self.get_url(sample_post.id)  # type: ignore
        response: Response = api_client.post(
            url,
            {
                "text": "try comment deleted post",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Comment.objects.count() == 0
