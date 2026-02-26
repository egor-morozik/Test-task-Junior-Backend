import pytest

from typing import Any

from rest_framework.test import APIClient

from core.models import Post


@pytest.fixture
def api_client() -> APIClient:
    """
    Фикстура для выполнения запросов к API бекенда.
    """

    return APIClient()


@pytest.fixture
def sample_post(db: Any) -> Post:
    """
    Фикстура для создания тестового поста в базе данных.
    """

    return Post.objects.create(
        ig_id="ig_12345",
        caption="some caption",
        permalink="https://inst.com",
        timestamp="2026-01-01T00:00:00Z",
    )
