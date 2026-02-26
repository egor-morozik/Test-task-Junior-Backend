from django.db import models


class InstagramBaseModel(models.Model):
    """
    Базовая модель сущностей Instagram.
    """

    ig_id = models.CharField(
        "ID в Instagram",
        max_length=100,
        unique=True,
        db_index=True,
    )  # type: ignore

    timestamp = models.DateTimeField(
        "Время создания в Instagram",
    )  # type: ignore

    db_created_at = models.DateTimeField(
        "Время добавления в базу данных",
        auto_now_add=True,
    )  # type: ignore

    class Meta:
        abstract = True
        ordering = [
            "-timestamp",
        ]
        indexes = [
            models.Index(
                fields=[
                    "-timestamp",
                ]
            ),
        ]


class Post(InstagramBaseModel):
    """
    Модель поста в Instagram.
    """

    caption = models.TextField(
        "Текст поста",
        blank=True,
        default="",
    )  # type: ignore

    media_url = models.URLField(
        "Ссылка на медиа",
        max_length=1000,
        blank=True,
        null=True,
    )  # type: ignore

    permalink = models.URLField(
        "Ссылка на пост",
        max_length=1000,
        blank=True,
        null=True,
    )  # type: ignore

    db_updated_at = models.DateTimeField(
        "Время последнего обновленния в БД",
        auto_now=True,
    )  # type: ignore


class Comment(InstagramBaseModel):
    """
    Модель комментария под постом Instagram.
    """

    post = models.ForeignKey(
        Post,
        related_name="comments",
        on_delete=models.CASCADE,
    )  # type: ignore

    text = models.TextField(
        "Текст комментария",
    )  # type: ignore

    username = models.CharField(
        "Автор",
        max_length=100,
    )  # type: ignore
