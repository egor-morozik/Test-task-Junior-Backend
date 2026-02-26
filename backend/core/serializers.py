from typing import Any, Dict

from rest_framework import serializers

from core.models import Post, Comment, InstagramBaseModel


class InstagramBaseSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для сущностей Instagram.
    """

    id = serializers.CharField(
        source="ig_id",
    )

    def save(self, **kwargs: Any) -> InstagramBaseModel:
        validated_data: Dict[str, Any] = {**self.validated_data, **kwargs}
        ig_id: str = validated_data.pop("ig_id")

        obj, _ = self.Meta.model.objects.update_or_create(  # type: ignore
            ig_id=ig_id,
            defaults=validated_data,
        )
        return obj


class CommentReadSerializer(InstagramBaseSerializer):
    """
    Сериализатор для чтения и синхронизации комментариев под постами Instagram.
    """

    class Meta:
        model = Comment
        fields = [
            "id",
            "text",
            "username",
            "timestamp",
            "db_created_at",
        ]


class CommentCreateSerializer(serializers.Serializer):
    """
    Сериализатор для входящих данных при создании комментария под пост Instagram.
    """

    text: serializers.CharField = serializers.CharField(
        required=True,
        max_length=1000,
    )


class PostSerializer(InstagramBaseSerializer):
    """
    Сериализатор для постов Instagram.
    """

    comments: CommentReadSerializer = CommentReadSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "caption",
            "media_url",
            "permalink",
            "timestamp",
            "db_created_at",
            "db_updated_at",
            "comments",
        ]
        extra_kwargs = {
            "caption": {
                "required": False,
                "allow_blank": True,
            },
            "media_url": {
                "required": False,
            },
            "permalink": {
                "required": False,
            },
        }
