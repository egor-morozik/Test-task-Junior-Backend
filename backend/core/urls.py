from typing import List

from django.urls import path, URLPattern

from core.views import SyncMediaView, PostListView, CommentCreateView


urlpatterns: List[URLPattern] = [
    path(
        "sync/",
        SyncMediaView.as_view(),
        name="sync-media",
    ),
    path(
        "posts/",
        PostListView.as_view(),
        name="post-list",
    ),
    path(
        "posts/<int:pk>/comment/",
        CommentCreateView.as_view(),
        name="comment-create",
    ),
]
