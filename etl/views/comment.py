from etl.serializers import *
from rest_framework import generics
from etl.models import *
from etl.permissions import *
from drf_yasg.utils import swagger_auto_schema
import etl.swaggers as swaggers


class CommentCreateView(generics.CreateAPIView):
    permission_classes = (IsAdminOrQualified,)
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['post_id'] = self.kwargs['pk']
        return context

    @swagger_auto_schema(
        operation_description=swaggers.post_comments_post_operation_description,
        request_body=swaggers.post_comments_post_request_body,
        responses=swaggers.post_comments_post_responses,
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminOrProfessorOrCreatorOrReadOnly,)
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()

    @swagger_auto_schema(
        operation_description=swaggers.comment_get_operation_description,
        responses=swaggers.comment_get_responses,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=swaggers.comment_patch_operation_description,
        request_body=swaggers.comment_patch_request_body,
        responses=swaggers.comment_patch_responses,
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=swaggers.comment_delete_operation_description,
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
