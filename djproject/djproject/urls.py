from django.urls import path
from .views import PostListCreateView, PostDetailView, CommentListCreateView, LikePostView

urlpatterns = [
    # Post URLs
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:post_id>/like/', LikePostView.as_view(), name='like-post'),

    # Comment URLs
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
]
