from rest_framework import generics
import rest_framework.permissions as permission_set
from etl.models import Post
from etl.serializers import PostListSerializer


class PostListCreateView(generics.ListCreateAPIView):
    permission_classes = [permission_set.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
