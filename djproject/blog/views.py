from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

# Pagination class
class PostPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

# Post Views
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-published_date')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PostPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'])

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs['post_id'])
        serializer.save(post=post)

class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        post.likes.add(request.user)
        return Response({'status': 'post liked'})

    def delete(self, request, post_id):
        post = Post.objects.get(id=post_id)
        post.likes.remove(request.user)
        return Response({'status': 'like removed'})

