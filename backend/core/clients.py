import requests

from typing import Any, Dict, Optional

from django.conf import settings


class InstagramClient:
    """
    HTTP-клиент для Instagram API.
    """

    API_VERSION: str = "v25.0"
    BASE_URL: str = f"https://graph.instagram.com/{API_VERSION}"

    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.params = {
            "access_token": settings.INSTAGRAM_ACCESS_TOKEN,
        }

    def _build_url(self, path: str) -> str:
        """
        Вспомогательный метод для сборки полного URL.
        """

        return f"{self.BASE_URL}/{path.lstrip('/')}"

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Базовый GET запрос.
        """

        response = self.session.get(
            self._build_url(path),
            params=params,
        )
        response.raise_for_status()
        return response.json()

    def post(self, path: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Базовый POST запрос.
        """

        response = self.session.post(
            self._build_url(path),
            data=data,
        )
        response.raise_for_status()
        return response.json()


instagram_client: InstagramClient = InstagramClient()
