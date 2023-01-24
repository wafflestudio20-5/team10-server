from etl.serializers import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from etl.models import *
from etl.permissions import *
from etl.paginations import *
from drf_yasg.utils import swagger_auto_schema
import etl.swaggers as swaggers


class QuestionListCreateView(generics.ListCreateAPIView):
    pagination_class = PostListPagination
    permission_classes = [IsAdmin | (IsAuthenticated & IsQualified)]
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(lecture_id=self.kwargs['pk']).filter(is_announcement=False)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['lecture_id'] = self.kwargs['pk']
        context['is_announcement'] = False
        return context

    @swagger_auto_schema(
        operation_description=swaggers.class_questions_get_operation_description,
        responses=swaggers.class_questions_get_responses,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=swaggers.class_questions_post_operation_description,
        request_body=swaggers.class_questions_post_request_body,
        responses=swaggers.class_questions_post_responses,
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin | (IsAuthenticated & IsQualified & (IsProfessor | IsCreatorReadOnly))]
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer

    @swagger_auto_schema(
        operation_description=swaggers.question_get_operation_description,
        responses=swaggers.question_get_responses,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=swaggers.question_patch_operation_description,
        request_body=swaggers.question_patch_request_body,
        responses=swaggers.question_patch_responses,
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=swaggers.question_delete_operation_description,
    )
    def delete(self, request, *args, **kwargs):

        return super().delete(request, *args, **kwargs)
